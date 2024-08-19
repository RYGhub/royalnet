use std::cmp::PartialEq;
use std::time::Duration;

use anyhow::Context;
use chrono::{DateTime, Local, TimeDelta, TimeZone};
use diesel::PgConnection;
use reqwest::Url;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{ChatId, LinkPreviewOptions, Message};
use tokio::time::sleep;

use crate::interfaces::database;
use crate::interfaces::database::models::{BroochMatch, DotaMatchId, TelegramUserId};
use crate::interfaces::stratz::{Byte, guild_matches, Short};
use crate::interfaces::stratz::guild_matches::{GameMode, Lane, LobbyType, Match, Player, Role, Steam};
use crate::services::RoyalnetService;
use crate::utils::anyhow_result::AnyResult;
use crate::utils::telegram_string::TelegramEscape;

#[derive(Debug, Clone)]
pub struct BroochService {
	database_url: String,
	graphql_url: Url,
	watched_guild_id: i64,
	min_players_to_process: usize,
	telegram_bot: Bot,
	notification_chat_id: ChatId,
	max_imp_wait: TimeDelta,
}

impl BroochService {
	#[allow(clippy::too_many_arguments)]
	pub fn new(
		database_url: String,
		graphql_base_url: &str,
		stratz_token: &str,
		watched_guild_id: i64,
		min_players_to_process: usize,
		telegram_bot_token: String,
		notification_chat_id: ChatId,
		max_imp_wait: TimeDelta
	)
		-> AnyResult<Self>
	{
		log::info!("Initializing a new Brooch service...");

		let mut graphql_url = Url::parse(graphql_base_url)
			.context("URL GraphQL non valido.")?;
		{
			let mut graphql_url_params = graphql_url.query_pairs_mut();
			graphql_url_params.append_pair("jwt", stratz_token);
		}

		log::trace!("Using GraphQL API URL: {graphql_url:?}");

		if min_players_to_process == 0 {
			anyhow::bail!("min_players_to_progress devono essere almeno 1.");
		}

		log::trace!("Processing only matches with at least {min_players_to_process} players.");

		let telegram_bot = Bot::new(telegram_bot_token);

		log::trace!("Using bot: {telegram_bot:#?}");

		log::trace!("Max IMP wait is: {max_imp_wait:?}");

		Ok(
			BroochService {
				database_url,
				graphql_url,
				watched_guild_id,
				min_players_to_process,
				telegram_bot,
				notification_chat_id,
				max_imp_wait,
			}
		)
	}

	fn create_http_client(&self) -> AnyResult<reqwest::Client> {
		log::debug!("Creating HTTP client...");

		reqwest::Client::builder()
			.build()
			.context("Impossibile creare un client HTTP appropriato a fare richieste all'API.")
	}

	fn create_postgres_connection(&self) -> AnyResult<PgConnection> {
		log::debug!("Creating PostgreSQL connection...");

		database::connect(&self.database_url)
			.context("Non è stato possibile connettersi al database RYG.")
	}

	async fn query_guild_matches(&self, client: &reqwest::Client) -> AnyResult<guild_matches::QueryResponse> {
		log::debug!("Querying for guild matches...");

		guild_matches::query(client, self.graphql_url.clone(), self.watched_guild_id)
			.await
			.context("Non è stato possibile recuperare le ultime partite di Dota da STRATZ.")
	}

	fn process_guild_data(&self, data: guild_matches::QueryResponse) -> AnyResult<guild_matches::Guild> {
		log::debug!("Processing guild data...");

		let data = data.data
			.context("La richiesta è riuscita, ma la risposta ricevuta da STRATZ era vuota.")?;

		let guild = data.guild
			.context("La richiesta è riuscita, ma non sono state ricevute gilde da STRATZ.")?;

		let guild_id: i64 = guild.id
			.context("La richiesta è riuscita, ma non è stato ricevuto l'ID della gilda da STRATZ.")?;

		log::trace!("Guild id is: {guild_id}");

		if guild_id != self.watched_guild_id {
			anyhow::bail!("La richiesta è riuscita, ma STRATZ ha risposto con le informazioni della gilda sbagliata.");
		}

		log::trace!("Guild id matches watched guild.");

		Ok(guild)
	}

	fn process_matches_data(&self, guild: guild_matches::Guild) -> AnyResult<Vec<Match>> {
		log::debug!("Processing matches data...");

		let mut matches = guild.matches
			.context("La richiesta è riuscita, ma non sono state ricevute informazioni sulle partite della gilda da STRATZ.")?
			.into_iter()
			.flatten()
			.collect::<Vec<Match>>();

		log::trace!("Received {} matches.", matches.len());

		log::trace!("Sorting matches by datetime...");

		// Sort matches chronologically
		matches.sort_unstable_by_key(|o| o
			.end_date_time
			.unwrap_or(0)
		);

		log::trace!("Sorted matches by datetime!");

		Ok(matches)
	}

	fn get_match_id(&self, r#match: &Match) -> AnyResult<DotaMatchId> {
		log::trace!("Getting match id...");

		Ok(
			r#match.id
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'ID della partita.")?
				.into()
		)
	}

	fn get_database_match(&self, database: &mut PgConnection, match_id: DotaMatchId) -> AnyResult<Option<BroochMatch>> {
		use crate::interfaces::database::query_prelude::*;
		use crate::interfaces::database::schema::brooch_match;

		log::trace!("Getting {match_id:?} from the database...");

		brooch_match::table
			.filter(brooch_match::id.eq(match_id))
			.get_result::<BroochMatch>(database)
			.optional()
			.context("Non è stato possibile recuperare la partita restituita da STRATZ dal database RYG.")
	}

	fn should_process_match_exists(&self, database: &mut PgConnection, match_id: DotaMatchId) -> AnyResult<bool> {
		log::trace!("Determining whether {match_id:?} should be processed...");

		self.get_database_match(database, match_id)
			.map(|m| m.is_none())
			.context("Non è stato possibile determinare se la partita restituita da STRATZ fosse stata già processata.")
	}

	fn get_match_datetime(&self, r#match: &Match) -> AnyResult<DateTime<Local>> {
		log::trace!("Getting match datetime...");

		let match_date = r#match.end_date_time
			.context("Non è stato ricevuto da STRATZ il momento di termine della partita.")?;

		log::trace!("Converting match datetime to local datetime...");

		Local.timestamp_opt(match_date, 0)
			.earliest()
			.context("È stato ricevuto da STRATZ un momento di termine della partita non valido.")
	}

	fn get_match_timedelta(&self, datetime: &DateTime<Local>) -> TimeDelta {
		log::trace!("Getting current time...");

		let now = Local::now();

		log::trace!("Getting match timedelta...");

		now - *datetime
	}

	fn get_match_type(&self, r#match: &Match) -> AnyResult<LobbyType> {
		log::trace!("Getting match type...");

		r#match.lobby_type.clone()
			.context("Non è stato ricevuta da STRATZ il tipo della partita.")
	}

	fn stringify_type(&self, r#type: LobbyType) -> String {
		use LobbyType::*;

		log::trace!("Stringifying match type: {:?}", r#type);

		match r#type {
			UNRANKED => String::from("Normale"),
			PRACTICE => String::from("Torneo"),
			TOURNAMENT => String::from("The International"),
			TUTORIAL => String::from("Tutorial"),
			COOP_VS_BOTS => String::from("Co-op"),
			TEAM_MATCH => String::from("Scontro di Clan"),
			SOLO_QUEUE => String::from("Coda solitaria"),
			RANKED => String::from("Classificata"),
			SOLO_MID => String::from("Duello"),
			BATTLE_CUP => String::from("Battle Cup"),
			EVENT => String::from("Evento"),
			DIRE_TIDE => String::from("Diretide"),
			Other(t) => t.clone(),
		}
	}

	fn get_match_mode(&self, r#match: &Match) -> AnyResult<GameMode> {
		log::trace!("Getting match mode...");

		r#match.game_mode.clone()
			.context("Non è stata ricevuta da STRATZ la modalità della partita.")
	}

	fn stringify_mode(&self, mode: GameMode) -> String {
		use GameMode::*;

		log::trace!("Stringifying match mode: {:?}", mode);

		match mode {
			NONE => String::from("Sandbox"),
			ALL_PICK => String::from("All Pick"),
			CAPTAINS_MODE => String::from("Captains Mode"),
			RANDOM_DRAFT => String::from("Random Draft"),
			SINGLE_DRAFT => String::from("Single Draft"),
			ALL_RANDOM => String::from("All Random"),
			INTRO => String::from("Tutorial"),
			THE_DIRETIDE => String::from("Diretide"),
			REVERSE_CAPTAINS_MODE => String::from("Reverse Captains"),
			THE_GREEVILING => String::from("The Greeviling"),
			TUTORIAL => String::from("Tutorial"),
			MID_ONLY => String::from("Mid Only"),
			LEAST_PLAYED => String::from("Least Played"),
			NEW_PLAYER_POOL => String::from("New Player"),
			COMPENDIUM_MATCHMAKING => String::from("Compendium"),
			CUSTOM => String::from("Arcade"),
			CAPTAINS_DRAFT => String::from("Captains Draft"),
			BALANCED_DRAFT => String::from("Balanced Draft"),
			ABILITY_DRAFT => String::from("Ability Draft"),
			EVENT => String::from("Evento"),
			ALL_RANDOM_DEATH_MATCH => String::from("All Random Deathmatch"),
			SOLO_MID => String::from("Mid Duel"),
			ALL_PICK_RANKED => String::from("All Draft"),
			TURBO => String::from("Turbo"),
			MUTATION => String::from("Mutation"),
			UNKNOWN => String::from("Unknown"),
			Other(t) => t.clone(),
		}
	}

	fn stringify_duration(&self, duration: TimeDelta) -> String {
		let minutes = duration.num_minutes();
		let seconds = duration.num_seconds() % 60;

		format!("{minutes:02}:{seconds:02}")
	}

	fn get_match_duration(&self, r#match: &Match) -> AnyResult<TimeDelta> {
		log::trace!("Getting match duration...");

		let secs = r#match.duration_seconds
			.context("Non è stata ricevuta da STRATZ la durata della partita.")?;

		log::trace!("Getting match duration timedelta...");

		let delta = TimeDelta::new(secs, 0)
			.context("Non è stato possibile rappresentare la durata della partita ricevuta da STRATZ.")?;

		Ok(delta)
	}

	fn get_match_players(&self, r#match: Match) -> AnyResult<Vec<Player>> {
		log::debug!("Getting match players...");

		let mut players: Vec<Player> = r#match.players
			.context("Non è stato ricevuto da STRATZ l'elenco dei giocatori della partita.")?
			.iter()
			.filter_map(|o| o.to_owned())
			.collect();

		log::trace!("Sorting match players...");

		players.sort_unstable_by_key(|o| match o.is_radiant.unwrap() {
			true => 1,
			false => 2,
		});

		log::trace!("Sorted match players!");

		Ok(players)
	}

	fn should_process_match_players(&self, players: &[Player]) -> bool {
		let players_len = players.len();

		log::trace!("Determining whether {players_len} are enough for the match to be processed...");

		players_len >= self.min_players_to_process
	}

	fn should_process_match_imp(&self, players: &[Player], timedelta: &TimeDelta) -> bool {
		log::trace!("Determining whether IMP is available for all players...");

		let imp_available_for_everyone = players.iter()
			.map(|o| o.imp)
			.map(|o| o.is_some())
			.all(|o| o);

		log::trace!("Determining whether enough time has passed for IMP to be ignored...");

		let imp_waited_too_long = *timedelta > self.max_imp_wait;

		imp_available_for_everyone || imp_waited_too_long
	}

	fn get_match_side(&self, players: &[Player]) -> AnyResult<MatchSide> {
		use MatchSide::*;

		log::debug!("Getting match side...");

		let mut side = None;

		for player in players.iter() {
			side = match (side, player.is_radiant) {
				(_, None) => {
					anyhow::bail!("Non è stata ricevuta da STRATZ la squadra di almeno uno dei giocatori.")
				},
				(None, Some(true)) => {
					Some(Radiant)
				},
				(None, Some(false)) => {
					Some(Dire)
				},
				(Some(Radiant), Some(true)) |
				(Some(Dire), Some(false)) => {
					side
				},
				(Some(Radiant), Some(false)) |
				(Some(Dire), Some(true)) => {
					Some(Both)
				},
				(Some(Both), _) => {
					break
				}
			}
		}

		let side = side.unwrap();

		log::trace!("Match side is: {side:?}");

		Ok(side)
	}
	
	fn get_match_outcome(&self, players: &[Player]) -> AnyResult<MatchOutcome> {
		use MatchOutcome::*;

		log::debug!("Getting match outcome...");

		let mut outcome = None;

		for player in players.iter() {
			outcome = match (outcome, player.is_victory) {
				(_, None) => {
					anyhow::bail!("Non è stata ricevuta da STRATZ la squadra di almeno uno dei giocatori.")
				},
				(None, Some(true)) => {
					Some(Victory)
				},
				(None, Some(false)) => {
					Some(Defeat)
				},
				(Some(Victory), Some(true)) |
				(Some(Defeat), Some(false)) => {
					outcome
				},
				(Some(Victory), Some(false)) |
				(Some(Defeat), Some(true)) => {
					Some(Clash)
				},
				(Some(Clash), _) => {
					break
				}
			}
		}

		let outcome = outcome.unwrap();

		log::trace!("Match outcome is: {outcome:?}");

		Ok(outcome)
	}

	fn get_player_steam(&self, player: &Player) -> AnyResult<Steam> {
		log::trace!("Getting player's Steam account...");

		player.steam_account.clone()
			.context("Non è stato ricevuto da STRATZ l'account Steam di almeno uno dei giocatori della partita.")
	}

	fn get_player_name(&self, steam: &Steam) -> AnyResult<String> {
		log::trace!("Getting player's Steam name...");

		steam.name.clone()
			.context("Non è stato ricevuto da STRATZ il display name di almeno uno dei giocatori della partita.")
	}

	fn get_player_telegram_id(&self, database: &mut PgConnection, player_steam: Steam) -> AnyResult<Option<TelegramUserId>> {
		use diesel::prelude::*;
		use diesel::{ExpressionMethods, QueryDsl};
		use crate::interfaces::database::schema::{steam, telegram, users};
		use crate::interfaces::database::models::TelegramUser;

		log::trace!("Getting player's Steam name...");

		let player_steam_id = player_steam.id
			.context("Non è stato ricevuto da STRATZ lo SteamID di almeno uno dei giocatori della partita.")?;

		log::trace!("Computing the two possible SteamIDs...");

		let player_steam_id_y0 = 0x_0110_0001_0000_0000 + player_steam_id;

		log::trace!("SteamID Y0 is: {player_steam_id_y0}");

		let player_steam_id_y1 = 0x_0110_0001_0000_0001 + player_steam_id;

		log::trace!("SteamID Y1 is: {player_steam_id_y1}");

		Ok(
			steam::table
				.inner_join(
					users::table.on(
						steam::user_id.eq(users::id)
					)
				)
				.inner_join(
					telegram::table.on(
						users::id.eq(telegram::user_id)
					)
				)
				.filter(
					steam::steam_id.eq(player_steam_id_y0)
				)
				.or_filter(
					steam::steam_id.eq(player_steam_id_y1)
				)
				.select(TelegramUser::as_select())
				.get_result::<TelegramUser>(database)
				.optional()
				.context("Non è stato possibile connettersi al database RYG.")?
				.map(|t| t.telegram_id)
		)
	}

	fn get_player_hero_name(&self, player: &Player) -> AnyResult<String> {
		log::trace!("Getting player's hero name...");

		player.hero.clone()
			.context("Non è stato ricevuto da STRATZ l'eroe giocato da almeno uno dei giocatori della partita.")?
			.display_name
			.context("Non è stato ricevuto da STRATZ il nome dell'eroe giocato da almeno uno dei giocatori della partita.")
	}

	fn get_player_outcome(&self, player: &Player) -> AnyResult<MatchOutcome> {
		use MatchOutcome::*;

		log::trace!("Getting player's match outcome...");

		let is_victory = &player.is_victory
			.context("Non è stato ricevuto da STRATZ il risultato della partita per almeno uno dei giocatori.")?;

		Ok(
			match is_victory {
				true => Victory,
				false => Defeat,
			}
		)
	}

	fn emojify_outcome(&self, outcome: MatchOutcome) -> &'static str {
		use MatchOutcome::*;

		log::trace!("Emojifying match outcome...");

		match outcome {
			Victory => "🟩",
			Defeat => "🔴",
			Clash => "💛",
		}
	}

	fn stringify_outcome(&self, outcome: MatchOutcome) -> &'static str {
		use MatchOutcome::*;

		log::trace!("Stringifying match outcome...");

		match outcome {
			Victory => "Vittoria!",
			Defeat => "Sconfitta...",
			Clash => "Derby",
		}
	}

	fn numberify_role_lane(role: &Option<Role>, lane: &Option<Lane>) -> u8 {
		use Role::*;
		use Lane::*;

		match (role, lane) {
			(         Some(CORE), Some(SAFE_LANE)) => 1,
			(         Some(CORE),  Some(MID_LANE)) => 2,
			(         Some(CORE),  Some(OFF_LANE)) => 3,
			(                  _,   Some(ROAMING)) => 4,
			(                  _,    Some(JUNGLE)) => 5,
			(Some(LIGHT_SUPPORT),               _) => 6,
			( Some(HARD_SUPPORT),               _) => 7,
			(                  _,               _) => 8,
		}
	}

	fn stringify_role_lane(&self, role: Role, lane: Lane) -> &'static str {
		use Role::*;
		use Lane::*;

		log::trace!("Stringifying role and lane...");

		match (role, lane) {
			(         CORE, SAFE_LANE) => "1️⃣ Safe Carry",
			(         CORE,  MID_LANE) => "2️⃣ Mid Carry",
			(         CORE,  OFF_LANE) => "3️⃣ Off Tank",
			(            _,   ROAMING) => "🔀 Roaming",
			(            _,    JUNGLE) => "⏫ Jungle",
			(LIGHT_SUPPORT,         _) => "4️⃣ Soft Support",
			( HARD_SUPPORT,         _) => "5️⃣ Hard Support",
			(            _,         _) => "🆕 Sconosciuto",
		}
	}

	fn emojify_imp(&self, imp: Short) -> &'static str {
		log::trace!("Emojifying IMP...");

		match imp {
			Short::MIN..=-49 => "🟧",
			-48..=-25 => "🔶",
			-24..=-1 => "🔸",
			0..=24 => "🔹",
			25..=48 => "🔷️",
			49..=Short::MAX => "🟦",
		}
	}

	fn emojify_kills_deaths_assists(&self, kills: Byte, deaths: Byte, assists: Byte) -> &'static str {
		log::trace!("Emojifying KDA...");

		let kills = kills as i16;
		let deaths = deaths as i16;
		let assists = assists as i16;

		let kda_score = kills + (assists / 2) - deaths;

		match kda_score {
			i16::MIN..=-1 => "➖",
			0..=i16::MAX => "➕",
		}
	}

	fn stringify_player(&self, database: &mut PgConnection, player: Player, show_outcome: bool) -> AnyResult<String> {
		log::debug!("Stringifying player...");
		log::trace!("Showing outcome: {show_outcome:?}");

		let steam = self.get_player_steam(&player)?;
		let name = self.get_player_name(&steam)?;
		let telegram_id = self.get_player_telegram_id(database, steam)?;
		let hero_name = self.get_player_hero_name(&player)?;
		let outcome = self.get_player_outcome(&player)?;

		let role = player.role.clone();
		let lane = player.lane.clone();
		let imp = player.imp;

		let kills = player.kills;
		let deaths = player.deaths;
		let assists = player.assists;

		// TODO: Buffs

		let mut lines = Vec::<String>::new();

		match telegram_id {
			None => lines.push(format!(
				"<u><b>{}</b> ({})</u>",
				name.escape_telegram_html(),
				hero_name.escape_telegram_html(),
			)),
			Some(telegram_id) => lines.push(format!(
				"<u><a href=\"tg://user?id={}\"><b>{}</b></a> ({})</u>",
				telegram_id.to_string().escape_telegram_html(),
				name.to_string().escape_telegram_html(),
				hero_name.to_string().escape_telegram_html(),
			)),
		}

		if show_outcome {
			lines.push(format!(
				"— {}", self.stringify_outcome(outcome)
			))
		}

		if let (Some(role), Some(lane)) = (role, lane) {
			lines.push(format!(
				"— {}", self.stringify_role_lane(role, lane)
			))
		}

		if let (Some(kills), Some(deaths), Some(assists)) = (kills, deaths, assists) {
			lines.push(format!(
				"— {} {kills} K / {deaths} D / {assists} A", self.emojify_kills_deaths_assists(kills, deaths, assists)
			))
		}

		if let Some(imp) = imp {
			lines.push(format!(
				"— {} {imp} IMP", self.emojify_imp(imp)
			))
		}

		Ok(lines.join("\n"))
	}

	fn stringify_match(&self, database: &mut PgConnection, r#match: Match) -> AnyResult<(DotaMatchId, Option<String>)> {
		log::debug!("Stringifying match...");

		let match_id = self.get_match_id(&r#match)?;

		if !self.should_process_match_exists(database, match_id)? {
			log::trace!("Skipping match, already parsed.");
			return Ok((match_id, None))
		}

		let datetime = self.get_match_datetime(&r#match)?;
		let timedelta = self.get_match_timedelta(&datetime);

		let r#type = self.get_match_type(&r#match)?;
		let mode = self.get_match_mode(&r#match)?;
		let duration = self.get_match_duration(&r#match)?;

		let mut players = self.get_match_players(r#match)?;

		if !self.should_process_match_players(&players) {
			log::trace!("Skipping match, not enough players.");
			return Ok((match_id, None))
		}
		
		if !self.should_process_match_imp(&players, &timedelta) {
			log::trace!("Skipping match, IMP is not ready.");
			return Ok((match_id, None))
		}

		players.sort_unstable_by_key(|a| Self::numberify_role_lane(&a.role, &a.lane));

		let _side = self.get_match_side(&players)?;
		let outcome = self.get_match_outcome(&players)?;

		let mut lines = Vec::<String>::new();

		lines.push(format!(
			"{} <u><b>{}</b></u>",
			self.emojify_outcome(outcome),
			self.stringify_outcome(outcome),
		));

		lines.push(format!(
			"<b>{}</b> · {} · <i>{}</i>",
			self.stringify_type(r#type),
			self.stringify_mode(mode),
			self.stringify_duration(duration),
		));

		lines.push("".to_string());

		for player in players.into_iter() {
			let string = self.stringify_player(database, player, outcome == MatchOutcome::Clash)?;
			lines.push(string);
			lines.push("".to_string());
		}

		lines.push(format!(
			"Partita <code>{}</code>",
			match_id,
		));

		Ok((match_id, Some(lines.join("\n"))))
	}

	async fn send_notification(&self, match_id: DotaMatchId, text: &str) -> AnyResult<Message> {
		log::debug!("Sending notification...");

		self.telegram_bot.send_message(self.notification_chat_id, text)
			.parse_mode(teloxide::types::ParseMode::Html)
			.disable_notification(true)
			.link_preview_options(LinkPreviewOptions {
				is_disabled: false,
				url: Some(format!("https://stratz.com/matches/{}", match_id)),
				prefer_small_media: true,
				prefer_large_media: false,
				show_above_text: false,
			})
			.await
			.context("Impossibile inviare la notifica di una partita.")
	}

	async fn iteration(&self) -> AnyResult<()> {
		log::debug!("Now running an iteration of brooch!");

		let client = self.create_http_client()?;
		let mut database = self.create_postgres_connection()?;

		let data = self.query_guild_matches(&client).await?;

		let guild = self.process_guild_data(data)?;
		let matches = self.process_matches_data(guild)?;

		let results = matches
			.into_iter()
			.map(|r#match| self.stringify_match(&mut database, r#match))
			.collect::<Vec<AnyResult<(DotaMatchId, Option<String>)>>>();

		for result in results {
			let (match_id, message) = result?;

			if let Some(message) = message {
				self.send_notification(match_id, &message).await?;
				BroochMatch::flag(&mut database, match_id)?;
			}
		}
		
		Ok(())
	}
}

impl RoyalnetService for BroochService {
	async fn run(&mut self) -> AnyResult<()> {
		loop {
			self.iteration().await?;

			sleep(Duration::new(60 * 15, 0)).await;
		}
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
