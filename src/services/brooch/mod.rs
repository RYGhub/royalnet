use std::convert::Infallible;
use anyhow::Result;
use std::future::Future;
use anyhow::Context;
use crate::services::RoyalnetService;
use crate::stratz::{GuildId, query_guild_matches};

mod config;

pub struct BroochService {
	guild_id: GuildId,
}

impl BroochService {
	async fn iteration(&self, client: reqwest::Client) -> Result<()> {
		let response = query_guild_matches(&client, &self.guild_id).await
			.context("Non è stato possibile recuperare le ultime partite di Dota da STRATZ.")?;

		let data = response.data
			.context("La richiesta è riuscita, ma la risposta ricevuta da STRATZ era vuota.")?;

		let data = data.guild
			.context("La richiesta è riuscita, ma non sono state ricevute gilde da STRATZ.")?;

		let id = data.name.clone()
			.context("La richiesta è riuscita, ma non è stato ricevuto l'ID della gilda da STRATZ.")?;

		let name = data.name.clone()
			.context("La richiesta è riuscita, ma non è stato ricevuto il nome della gilda da STRATZ.")?;

		let data = data.matches
			.context("La richiesta è riuscita, ma non sono state ricevute informazioni sulle partite della gilda da STRATZ.")?;

		for r#match in data {
			let r#match = r#match
				.context("La richiesta è riuscita, ma non è stato possibile processare una delle partite restituite da STRATZ.")?;

			let match_id = r#match.id.clone()
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'ID di una delle partite.")?;

			let match_duration = r#match.duration_seconds.clone()
				.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la durata di una delle partite.")?;

			let match_date = r#match.end_date_time.clone()
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il momento di termine di una delle partite.")?;

			let match_mode = r#match.game_mode.clone()
				.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la modalità di una delle partite.")?;

			let match_type = r#match.lobby_type.clone()
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il tipo di una delle partite.")?;

			let players = r#match.players
				.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'elenco dei giocatori di una delle partite.")?;

			for player in players {
				let player = player
					.context("La richiesta è riuscita, ma non sono stati ricevuti da STRATZ i dettagli di almeno uno dei giocatori delle partite.")?;

				let player_steam = player.steam_account.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'account Steam di almeno uno dei giocatori delle partite.")?;

				let player_kills = player.kills.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di uccisioni di almeno uno dei giocatori delle partite.")?;

				let player_deaths = player.deaths.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di morti di almeno uno dei giocatori delle partite.")?;

				let player_assists = player.assists.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il numero di aiuti di almeno uno dei giocatori delle partite.")?;

				let player_imp = player.imp.clone();

				let player_hero = player.hero.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ l'eroe giocato da almeno uno dei giocatori delle partite.")?;

				let player_is_radiant = player.is_radiant.clone()
					.context("La richiesta è riuscita, ma non è stata ricevuta da STRATZ la squadra di almeno uno dei giocatori delle partite.")?;

				let player_is_victory = player.is_victory.clone()
					.context("La richiesta è riuscita, ma non è stato ricevuto da STRATZ il vincitore di almeno una delle partite.")?;
			}
		}

		Ok(())
	}
}

impl RoyalnetService for BroochService {
	#[allow(unreachable_code)]
	async fn run(self) -> anyhow::Result<Infallible> {
		let client = reqwest::Client::new();

		loop {
			self.iteration(client).await?;
		}

		anyhow::bail!("Brooch service has exited.")
	}
}