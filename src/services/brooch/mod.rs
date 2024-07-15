use std::convert::Infallible;
use anyhow::Result;
use std::time::Duration;
use anyhow::Context;
use chrono::{TimeDelta, TimeZone};
use diesel::RunQueryDsl;
use tokio::time::sleep;
use crate::database;
use crate::database::models::{BroochMatch, RoyalnetUser};
use crate::services::RoyalnetService;
use crate::stratz::{Guild, GuildId, Player, query_guild_matches};

mod config;

pub struct BroochService {
	guild_id: GuildId,
}

impl BroochService {
	async fn iteration(&self) -> Result<()> {
		let client = reqwest::Client::new();

		let mut database = database::connect()
			.context("Non è stato possibile connettersi al database RYG.")?;

		let response = query_guild_matches(&client, &self.guild_id).await
			.context("Non è stato possibile recuperare le ultime partite di Dota da STRATZ.")?;

		let data = response.data
			.context("La richiesta è riuscita, ma la risposta ricevuta da STRATZ era vuota.")?;

		let data = data.guild
			.context("La richiesta è riuscita, ma non sono state ricevute gilde da STRATZ.")?;

		let guild_id: GuildId = data.id.clone()
			.context("La richiesta è riuscita, ma non è stato ricevuto l'ID della gilda da STRATZ.")?
			.into();

		if guild_id != *config::BROOCH_WATCHED_GUILD_ID() {
			anyhow::bail!("La richiesta è riuscita, ma STRATZ ha risposto con le informazioni della gilda sbagliata.");
		}

		let guild_name = data.name.clone()
			.context("La richiesta è riuscita, ma non è stato ricevuto il nome della gilda da STRATZ.")?;

		let mut matches = data.matches
			.context("La richiesta è riuscita, ma non sono state ricevute informazioni sulle partite della gilda da STRATZ.")?;

		matches.sort_unstable_by_key(|o| o
			.to_owned()
			.map(|o| o
				.end_date_time
				.unwrap_or(0)
			)
			.unwrap_or(0)
		);

		for r#match in matches {
			let r#match = r#match
				.context("La richiesta è riuscita, ma non è stato possibile processare una delle partite restituite da STRATZ.")?;

			let match_royalnet = {
				use diesel::prelude::*;
				use diesel::{ExpressionMethods, QueryDsl};
				use crate::database::schema::brooch_match::dsl::*;

				brooch_match
					.filter(id.eq(match_id))
					.select(BroochMatch::as_select())
					.get_result(&mut database)
					.optional()
					.context("Non è stato possibile recuperare almeno una delle partite restituite da STRATZ dal database RYG.")?
			};

			let match_royalnet = match match_royalnet {
				None => {
					log::trace!("Match result was already sent, skipping...");
					continue
				},
				Some(v) => v,
			};

			let mut text = String::new();

			let match_duration = r#match.duration_seconds
				.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la durata di una delle partite.")?;

			let match_date = r#match.end_date_time
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il momento di termine di una delle partite.")?;

			let match_date = chrono::Utc.timestamp_opt(match_date, 0)
				.earliest()
				.context("La richiesta è riuscita, ma è stato ricevuto da STRATZ un momento di termine di una delle partite non valido.")?;

			let now = chrono::Utc::now();

			let match_offset = match_date - now;

			let match_mode = r#match.game_mode.clone()
				.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la modalità di almeno una delle partite.")?;

			let match_type = r#match.lobby_type.clone()
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il tipo di almeno una delle partite.")?;

			let players = r#match.players
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'elenco dei giocatori di almeno una delle partite.")?;

			let mut players: Vec<Player> = players
				.iter()
				.filter_map(|o| o.to_owned())
				.collect();

			if players.len() < 1 {
				anyhow::bail!("La richiesta è riuscita, ma è stato ricevuto da STRATZ un elenco vuoto di giocatori per una delle partite.")?;
			}

			let imp_is_ready = players.iter().map(|o| o.imp).all(|o| o.is_some());
			let imp_wait_too_long = match_offset > TimeDelta::minutes(60);

			if imp_wait_too_long {
				log::trace!("Imp is not ready, but the wait was too long, so we're assuming it's just not available")
			}
			else if !imp_is_ready {
				log::trace!("Imp is not ready, waiting a bit more...");
				continue
			}

			let match_radiant = r#match.did_radiant_win.clone()
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il vincitore di almeno una delle partite")?;

			players.sort_unstable_by_key(|o| o
				.to_owned()
				.map(|o| o
					.is_radiant
					.unwrap_or(false)
				)
				.unwrap_or(false)
			);

			{
				let match_id = r#match.id
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'ID di una delle partite.")?;

				let match_outcome = 'outcome: {
					let mut players_radiant: Option<bool> = None;
					for player in players {
						let player_radiant = player.is_radiant
							.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la squadra di almeno uno dei giocatori delle partite.")?;

						if players_radiant.is_none() {
							players_radiant = Some(player_radiant)
						} else {
							if players_radiant != player_radiant {
								break 'outcome MatchOutcome::Clash;
							}
						}
					};

					if players_radiant ^ match_radiant {
						MatchOutcome::Defeat
					} else {
						MatchOutcome::Victory
					}
				};

				text.push_str(format!(
					r#"{} <a href="https://stratz.com/matches/{}"><b><u>Partita #{}</u></b></a>\n"#,
					match_outcome.emoji(),
					match_id,
					match_id,
				));
			}


			for player in players {
				let player_steam = player.steam_account.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'account Steam di almeno uno dei giocatori delle partite.")?;

				let player_steam_id = player_steam.id
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ lo SteamID di almeno uno dei giocatori delle partite.")?;

				let player_steam_name = player_steam.name
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il display name di almeno uno dei giocatori delle partite.")?;

				let player_royalnet: RoyalnetUser = {
					use diesel::prelude::*;
					use diesel::{ExpressionMethods, QueryDsl};
					use crate::database::schema::steam::dsl::*;
					use crate::database::schema::users::dsl::*;
					use crate::database::models::RoyalnetUser;

					steam
						.filter(steam_id.eq(player_steam_id))
						.inner_join(users)
						.select(RoyalnetUser::as_select())
						.get_result(&mut database)
						.context("Non è stato possibile recuperare il tuo utente Telegram dal database RYG.")?
				};

				let player_kills = player.kills
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di uccisioni di almeno uno dei giocatori delle partite.")?;

				let player_deaths = player.deaths
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di morti di almeno uno dei giocatori delle partite.")?;

				let player_assists = player.assists
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di aiuti di almeno uno dei giocatori delle partite.")?;

				let player_imp = player.imp;

				let player_hero = player.hero.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'eroe giocato da almeno uno dei giocatori delle partite.")?;

				let player_is_radiant = player.is_radiant
					.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la squadra di almeno uno dei giocatori delle partite.")?;

				let player_stats = player.stats.clone()
					.context("La richiesta è riuscita, ma non sono state ricevute da STRATZ le statistiche di almeno uno dei giocatori delle partite.")?;

				let player_buffs = player_stats.match_player_buff_event.clone()
					.unwrap_or_default();

				for buff in player_buffs.iter().filter_map(|s| s.to_owned()) {

				}
			}
		}

		Ok(())
	}
}

impl RoyalnetService for BroochService {
	#[allow(unreachable_code)]
	async fn run(self) -> Result<Infallible> {
		loop {
			self.iteration().await?;

			sleep(Duration::new(60 * 15, 0)).await;
		}

		anyhow::bail!("Brooch service has exited.")
	}
}

pub enum MatchOutcome {
	Victory,
	Defeat,
	Clash,
}

impl MatchOutcome {
	pub fn emoji(&self) -> &'static str {
		match self {
			MatchOutcome::Victory => "🟢",
			MatchOutcome::Defeat => "🟥",
			MatchOutcome::Clash => "🔶",
		}
	}
}
