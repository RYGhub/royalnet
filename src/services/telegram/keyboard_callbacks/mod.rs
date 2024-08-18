mod matchmaking;

use std::str::FromStr;
use std::sync::Arc;
use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::AnswerCallbackQuerySetters;
use teloxide::prelude::CallbackQuery;
use teloxide::requests::Requester;
use crate::services::telegram::utils::matchmaking::{MatchmakingTelegramKeyboardCallback};
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum KeyboardCallback {
	Matchmaking(i32, MatchmakingTelegramKeyboardCallback),
}

impl FromStr for KeyboardCallback {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		let (keyword, data) = s.split_once(":")
			.context("Impossibile dividere il payload in keyword e dati.")?;

		let (id, data) = data.split_once(":")
			.context("Impossibile dividere il payload in id e dati.")?;

		let id: i32 = id.parse()
			.context("Impossibile convertire l'id a un numero.")?;

		match keyword {
			"matchmaking" => {
				data
					.parse()
					.map(|c| Self::Matchmaking(id, c))
					.context("Impossibile processare i dati.")
			},
			x => {
				anyhow::bail!("Keyword sconosciuta: {x:?}")
			}
		}
	}
}

impl KeyboardCallback {
	pub async fn handle_self(self, bot: Bot, query: CallbackQuery, database: Arc<DatabaseInterface>) -> KeyboardCallbackResult {
		log::debug!("Handling keyboard callback...");

		log::trace!(
			"Handling {:?} in {:?} with {:?}...",
			self,
			&query.message.as_ref().map(|q| q.chat.id),
			&query.id,
		);

		match self {
			Self::Matchmaking(matchmaking_id, callback) => {
				matchmaking::handler(&bot, query, matchmaking_id, callback, &database).await?
			}
		}

		log::trace!("Successfully handled keyboard callback!");
		Ok(())
	}

	pub async fn handle_unknown(bot: Bot, query: CallbackQuery) -> KeyboardCallbackResult {
		log::warn!("Received an unknown keyboard callback: {:#?}", &query.data);

		bot
			.answer_callback_query(query.id)
			.show_alert(true)
			.text("⚠️ Il tasto che hai premuto non è più valido.")
			.await?;

		log::trace!("Successfully handled unknown keyboard callback!");
		Ok(())
	}
}

type KeyboardCallbackResult = anyhow::Result<()>;
