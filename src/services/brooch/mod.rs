use std::cmp::PartialEq;
use std::convert::Infallible;
use anyhow::Result;
use std::time::Duration;
use anyhow::Context;
use chrono::{TimeDelta, TimeZone};
use diesel::PgConnection;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use tokio::time::sleep;
use crate::database;
use crate::services::RoyalnetService;
use crate::stratz::{GuildId, Match, Player, Role, Lane, query_guild_matches};
use crate::stratz::guild_matches_query::{GameModeEnumType, LobbyTypeEnum};

mod config;

pub struct BroochService {
	pub guild_id: GuildId,
	pub bot: Bot,
}

impl BroochService {
	const MAX_IMP_WAIT: TimeDelta = TimeDelta::minutes(60);

	pub fn from_config() -> Self {
		Self {
			guild_id: config::BROOCH_WATCHED_GUILD_ID().clone(),
			bot: Bot::new(config::BROOCH_TELEGRAM_BOT_TOKEN().clone()),
		}
	}

	async fn iteration_request(&self) -> Result<()> {
		let client = reqwest::Client::new();

		let mut database = database::connect()
			.context("Non è stato possibile connettersi al database RYG.")?;

		let data = query_guild_matches(&client, &self.guild_id).await
			.context("Non è stato possibile recuperare le ultime partite di Dota da STRATZ.")?;

		let data = data.data
			.context("La richiesta è riuscita, ma la risposta ricevuta da STRATZ era vuota.")?;

		let data = data.guild
			.context("La richiesta è riuscita, ma non sono state ricevute gilde da STRATZ.")?;

		let guild_id: GuildId = data.id.clone()
			.context("La richiesta è riuscita, ma non è stato ricevuto l'ID della gilda da STRATZ.")?
			.into();

		if guild_id != self.guild_id {
			anyhow::bail!("La richiesta è riuscita, ma STRATZ ha risposto con le informazioni della gilda sbagliata.");
		}

		let mut matches = data.matches
			.context("La richiesta è riuscita, ma non sono state ricevute informazioni sulle partite della gilda da STRATZ.")?;

		// Sort matches chronologically
		matches.sort_unstable_by_key(|o| o
			.to_owned()
			.map(|o| o
				.end_date_time
				.unwrap_or(0)
			)
			.unwrap_or(0)
		);

		let mut results: Vec<Result<(i64, Option<String>)>> = vec![];

		for r#match in matches.iter().filter_map(|o| o.to_owned()) {
			results.push(
				self.iteration_match(&mut database, r#match).await
			);
		}

		let chat_id = config::BROOCH_NOTIFICATION_CHAT_ID();

		let results: Vec<(i64, String)> = results
			.into_iter()
			.inspect(|f| match f {
				Err(e) => log::error!("Error while processing match: {e}"),
				Ok((match_id, None)) => log::debug!("Skipping: {match_id}"),
				_ => {}
			})
			.filter_map(|f| f.ok())
			.filter_map(|f| f.1.map(|s| (f.0, s)))
			.collect();

		for result in results {
			let (match_id, text) = result;

			let msg = self.bot.send_message(*chat_id, text)
				.parse_mode(teloxide::types::ParseMode::Html)
				.disable_notification(true)
				.disable_web_page_preview(true)
				.await;

			if let Err(e) = msg {
				log::error!("Error while sending notification for match {match_id}: {e}");
				continue
			}

			{
				use diesel::prelude::*;
				use crate::database::schema::brooch_match::dsl::*;
				use crate::database::models::{BroochMatch};

				let match_royalnet = BroochMatch { id: result.0 };

				let result = diesel::insert_into(brooch_match)
					.values(&match_royalnet)
					.returning(BroochMatch::as_returning())
					.get_result(&mut database);

				if let Err(e) = result {
					log::error!("Error while inserting in database match {match_id}: {e}");
					continue
				}

				log::trace!("Inserted in database match {match_id}!");
			}
		}

		Ok(())
	}

	async fn iteration_match(&self, database: &mut PgConnection, r#match: Match) -> Result<(i64, Option<String>)> {
		let match_id = r#match.id
			.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'ID della partita.")?;

		let match_royalnet = {
			use diesel::prelude::*;
			use diesel::{ExpressionMethods, QueryDsl};
			use crate::database::schema::brooch_match::dsl::*;
			use crate::database::models::{BroochMatch};

			brooch_match
				.filter(id.eq(match_id))
				.select(BroochMatch::as_select())
				.get_result(database)
				.optional()
				.context("Non è stato possibile recuperare la partita restituita da STRATZ dal database RYG.")?
		};

		if match_royalnet.is_some() {
			log::trace!("Match result was already sent, skipping...");
			return Ok((match_id, None));
		};

		let match_date = r#match.end_date_time
			.context("Non è stato ricevuto da STRATZ il momento di termine della partita.")?;

		let match_date = chrono::Utc.timestamp_opt(match_date, 0)
			.earliest()
			.context("È stato ricevuto da STRATZ un momento di termine della partita non valido.")?;

		let now = chrono::Utc::now();

		// How much time has passed since the match has ended?
		let match_offset = match_date - now;

		let mut players: Vec<Player> = r#match.players
			.context("Non è stato ricevuto da STRATZ l'elenco dei giocatori della partita.")?
			.iter()
			.filter_map(|o| o.to_owned())
			.collect();

		if players.len() < 1 {
			anyhow::bail!("È stato ricevuto da STRATZ un elenco vuoto di giocatori nella partita.");
		}

		let match_side: MatchSide = 'side: {
			let players_teams = {
				let players_teams_inner: Vec<Option<bool>> = players.iter()
					.map(|o| o.is_radiant)
					.collect();

				for player_team in players_teams_inner.iter() {
					if player_team.is_none() {
						player_team.context("Non è stata ricevuta da STRATZ la squadra di almeno un giocatore nella partita.")?;
					}
				}

				let players_teams_inner: Vec<bool> = players_teams_inner
					.iter()
					.map(|o| o.unwrap())
					.collect();

				players_teams_inner
			};

			let mut predicted_team = None;

			for player_team in players_teams {
				if predicted_team.is_none() {
					predicted_team = Some(player_team)
				}
				else if predicted_team.unwrap() != player_team {
					break 'side MatchSide::Both;
				}
			}

			match predicted_team.unwrap() {
				true => MatchSide::Radiant,
				false => MatchSide::Dire,
			}
		};

		// Is IMP available?
		let imp_is_ready = players.iter()
			.map(|o| o.imp)
			.map(|o| o.is_some())
			.all(|o| o);

		// Have we waited too long for IMP to be calculated?
		let imp_wait_too_long = match_offset > Self::MAX_IMP_WAIT;

		if !(imp_is_ready || imp_wait_too_long) {
			log::trace!("IMP is not ready, waiting a bit more...");
			// Let's wait some more.
			return Ok((match_id, None));
		}

		let match_radiant_win = r#match.did_radiant_win
			.context("Non è stato ricevuto da STRATZ il vincitore della partita.")?;

		let match_outcome = MatchOutcome::from(&match_side, match_radiant_win);

		let match_outcome_emoji = match_outcome.emoji();

		let match_type = r#match.lobby_type.clone()
			.context("Non è stato ricevuta da STRATZ il tipo della partita.")?;

		let match_type_str = match match_type {
			LobbyTypeEnum::UNRANKED => "Normale",
			LobbyTypeEnum::PRACTICE => "Torneo",
			LobbyTypeEnum::TOURNAMENT => "The International",
			LobbyTypeEnum::TUTORIAL => "Tutorial",
			LobbyTypeEnum::COOP_VS_BOTS => "Co-op",
			LobbyTypeEnum::TEAM_MATCH => "Scontro di Clan",
			LobbyTypeEnum::SOLO_QUEUE => "Coda solitaria",
			LobbyTypeEnum::RANKED => "Classificata",
			LobbyTypeEnum::SOLO_MID => "Duello",
			LobbyTypeEnum::BATTLE_CUP => "Battle Cup",
			LobbyTypeEnum::EVENT => "Evento",
			LobbyTypeEnum::DIRE_TIDE => "Diretide",
			LobbyTypeEnum::Other(t) => anyhow::bail!("Il tipo di partita ricevuto da STRATZ è sconosciuto: {}", t)
		};

		let match_mode = r#match.game_mode.clone()
			.context("Non è stata ricevuta da STRATZ la modalità della partita.")?;

		let match_mode_str = match match_mode {
			GameModeEnumType::NONE => "Sandbox",
			GameModeEnumType::ALL_PICK => "All Pick",
			GameModeEnumType::CAPTAINS_MODE => "Captains Mode",
			GameModeEnumType::RANDOM_DRAFT => "Random Draft",
			GameModeEnumType::SINGLE_DRAFT => "Single Draft",
			GameModeEnumType::ALL_RANDOM => "All Random",
			GameModeEnumType::INTRO => "Tutorial",
			GameModeEnumType::THE_DIRETIDE => "Diretide",
			GameModeEnumType::REVERSE_CAPTAINS_MODE => "Reverse Captains",
			GameModeEnumType::THE_GREEVILING => "The Greeviling",
			GameModeEnumType::TUTORIAL => "Tutorial",
			GameModeEnumType::MID_ONLY => "Mid Only",
			GameModeEnumType::LEAST_PLAYED => "Least Played",
			GameModeEnumType::NEW_PLAYER_POOL => "New Player",
			GameModeEnumType::COMPENDIUM_MATCHMAKING => "Compendium",
			GameModeEnumType::CUSTOM => "Arcade",
			GameModeEnumType::CAPTAINS_DRAFT => "Captains Draft",
			GameModeEnumType::BALANCED_DRAFT => "Balanced Draft",
			GameModeEnumType::ABILITY_DRAFT => "Ability Draft",
			GameModeEnumType::EVENT => "Evento",
			GameModeEnumType::ALL_RANDOM_DEATH_MATCH => "All Random Deathmatch",
			GameModeEnumType::SOLO_MID => "Mid Duel",
			GameModeEnumType::ALL_PICK_RANKED => "All Draft",
			GameModeEnumType::TURBO => "Turbo",
			GameModeEnumType::MUTATION => "Mutation",
			GameModeEnumType::UNKNOWN => anyhow::bail!("La modalità di partita ricevuto da STRATZ è sconosciuta."),
			GameModeEnumType::Other(t) => anyhow::bail!("Il tipo di partita ricevuto da STRATZ è sconosciuta: {}", t)
		};

		let match_duration = r#match.duration_seconds
			.context("Non è stata ricevuta da STRATZ la durata della partita.")?;

		// Let's begin writing the message
		let mut text = format!(
			"{match_outcome_emoji} <a href=\"https://stratz.com/matches/{match_id}\"><b><u>Partita #{match_id}</u></b></a>\n\
			<b>{match_type_str}</b> · {match_mode_str} · <i>{match_duration}</i>\n\
			\n\
			",
		);

		// Let's sort players by team...
		players.sort_unstable_by_key(|o| match o.is_radiant.unwrap() {
			true => 1,
			false => 2,
		});

		for player in players {
			let player_steam = player.steam_account.clone()
				.context("Non è stato ricevuto da STRATZ l'account Steam di almeno uno dei giocatori della partita.")?;

			let player_steam_id = player_steam.id
				.context("Non è stato ricevuto da STRATZ lo SteamID di almeno uno dei giocatori della partita.")?;

			let player_steam_name = player_steam.name
				.context("Non è stato ricevuto da STRATZ il display name di almeno uno dei giocatori della partita.")?;

			let player_hero = player.hero.clone()
				.context("Non è stato ricevuto da STRATZ l'eroe giocato da almeno uno dei giocatori della partita.")?;

			let player_hero_name = player_hero.display_name
				.context("Non è stato ricevuto da STRATZ il nome dell'eroe giocato da almeno uno dei giocatori della partita.")?;


			let player_telegram = {
				use diesel::prelude::*;
				use diesel::{ExpressionMethods, QueryDsl};
				use crate::database::schema::steam::dsl::*;
				use crate::database::schema::users::dsl::*;
				use crate::database::schema::telegram::dsl::*;
				use crate::database::models::TelegramUser;

				steam
					.filter(steam_id.eq(player_steam_id))
					.inner_join(users
						.inner_join(telegram)
					)
					.select(TelegramUser::as_select())
					.get_result(database)
					.optional()
					.ok()
					.flatten()
			};

			let player_telegram_id = player_telegram
				.map(|t| t.telegram_id);

			text.push_str(
				&match player_telegram_id {
					Some(player_telegram_id) => format!(
						"<a href=\"tg://user?id={player_telegram_id}\"><b>{player_steam_name}</b></a> ({player_hero_name})\n"
					),
					None => format!(
						"<b>{player_steam_name}</b> ({player_hero_name})\n"
					),
				});

			let player_role: Option<Role> = player.role.clone();
			let player_lane: Option<Lane> = player.lane.clone();

			if let Some(player_role) = player_role {
				if let Some(player_lane) = player_lane {
					text.push_str(
						match (player_role, player_lane) {
							(Role::CORE, Lane::SAFE_LANE) => "— 1️⃣ Safe Carry\n",
							(Role::CORE, Lane::MID_LANE) => "— 2️⃣ Mid Carry\n",
							(Role::CORE, Lane::OFF_LANE) => "— 3️⃣ Off Carry\n",
							(Role::LIGHT_SUPPORT, _) => "— 4️⃣ Soft Support\n",
							(Role::HARD_SUPPORT, _) => "— 5️⃣ Hard Support\n",
							(_, Lane::JUNGLE) => "— 🔼 Jungle\n",
							(_, Lane::ROAMING) => "— 🔀 Roaming\n",
							_ => "",
						}
					);
				}
			}

			let player_imp = player.imp;

			let player_imp_emoji = 'emoji: {
				if player_imp.is_none() {
					break 'emoji ""
				}
				let player_imp = player_imp.unwrap();
				if player_imp < -50 {
					"🔲"
				} else if player_imp < -25 {
					"⬛️"
				} else if player_imp < -18 {
					"◼️"
				} else if player_imp < -9 {
					"◾️"
				} else if player_imp < 0 {
					"▪️"
				} else if player_imp <= 9 {
					"▫️"
				} else if player_imp <= 18 {
					"◽️"
				} else if player_imp <= 25 {
					"◻️"
				} else if player_imp <= 50 {
					"⬜️"
				} else {
					"🔳"
				}
			};

			let player_kills = player.kills
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di uccisioni di almeno uno dei giocatori delle partite.")?;

			let player_deaths = player.deaths
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di morti di almeno uno dei giocatori delle partite.")?;

			let player_assists = player.assists
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di aiuti di almeno uno dei giocatori delle partite.")?;

			text.push_str(&match player_imp {
				Some(player_imp) => format!(
					"— {player_imp_emoji} {player_imp} IMP ({player_kills}/{player_deaths}/{player_assists})\n"
				),
				None => format!(
					"— ❔ {player_kills}/{player_deaths}/{player_assists}\n"
				),
			});

			if match_outcome == MatchOutcome::Clash {
				let player_is_radiant = player.is_radiant.unwrap();

				text.push_str(match (match_radiant_win, player_is_radiant) {
					(true, true) => "🟢 Vittoria!\n",
					(false, false) => "🟢 Vittoria!\n",
					(true, false) => "🟥 Sconfitta...\n",
					(false, true) => "🟥 Sconfitta...\n",
				})
			}

			let player_stats = player.stats.clone()
				.context("La richiesta è riuscita, ma non sono state ricevute da STRATZ le statistiche di almeno uno dei giocatori delle partite.")?;

			let player_buffs = player_stats.match_player_buff_event.clone()
				.unwrap_or_default();

			for _buff in player_buffs.iter().filter_map(|s| s.to_owned()) {
				// TODO: Let's do this another time.
			}

			text.push_str("\n")
		}

		Ok((match_id, Some(text)))
	}
}

impl RoyalnetService for BroochService {
	#[allow(unreachable_code)]
	async fn run(self) -> Result<Infallible> {
		loop {
			self.iteration_request().await?;

			sleep(Duration::new(60 * 15, 0)).await;
		}

		anyhow::bail!("Brooch service has exited.")
	}
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchSide {
	Radiant,
	Dire,
	Both,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchOutcome {
	Victory,
	Defeat,
	Clash,
}

impl MatchOutcome {
	pub fn from(side: &MatchSide, radiant_win: bool) -> Self {
		match (side, radiant_win) {
			(MatchSide::Both, _) => Self::Clash,
			(MatchSide::Radiant, true) => Self::Victory,
			(MatchSide::Radiant, false) => Self::Defeat,
			(MatchSide::Dire, true) => Self::Defeat,
			(MatchSide::Dire, false) => Self::Victory,
		}
	}

	pub fn emoji(&self) -> &'static str {
		match self {
			MatchOutcome::Victory => "🟢",
			MatchOutcome::Defeat => "🟥",
			MatchOutcome::Clash => "🔶",
		}
	}
}
