// See the following link for an example of how to use this file:
// https://github.com/teloxide/teloxide/blob/master/crates/teloxide/examples/dispatching_features.rs

use std::sync::Arc;
use anyhow::{Context, Error, Result};
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::Message;
use teloxide::utils::command::BotCommands;
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;

pub mod start;
pub mod fortune;
pub mod echo;
pub mod help;
pub mod whoami;
pub mod answer;
pub mod reminder;
pub mod dog;
pub mod cat;
pub mod roll;
pub mod diario;
pub mod matchmaking;

#[derive(Debug, Clone, PartialEq, Eq, BotCommands)]
#[command(rename_rule = "lowercase")]
pub enum Command {
	#[command(description = "Invia messaggio di introduzione.")]
	Start,
	#[command(description = "Visualizza l'elenco dei comandi disponibili, o mostra informazioni su uno specifico comando.")]
	Help(String),
	#[command(description = "Mostra il tuo oroscopo di oggi.")]
	Fortune,
	#[command(description = "Ripeti il testo inviato.")]
	Echo(String),
	#[command(description = "Controlla a che account RYG è associato il tuo account Telegram.")]
	WhoAmI,
	#[command(description = "Rispondi ad una domanda.")]
	Answer(String),
	#[command(description = "Ricorda la chat di qualcosa che avverrà in futuro. Non persiste ai riavvii del bot.")]
	Reminder(reminder::ReminderArgs),
	#[command(description = "Invia un cane casuale in chat.")]
	Dog,
	#[command(description = "Invia un gatto casuale in chat.")]
	Cat,
	#[command(description = "Tira un dado.")]
	Roll(String),
	#[command(description = "Salva una citazione nel diario RYG.")]
	Diario(diario::DiarioArgs),
	#[command(description = "Chiedi chi è disponibile per giocare a qualcosa.")]
	Matchmaking(matchmaking::MatchmakingArgs),
}

impl Command {
	pub async fn set_commands(bot: &mut Bot) -> Result<()> {
		log::trace!("Determining bot commands...");
		let commands = Self::bot_commands();

		// This always returns true, for whatever reason
		log::trace!("Setting commands: {commands:#?}");
		let _ = bot.set_my_commands(commands).await
			.context("Impossibile aggiornare l'elenco comandi del bot.")?;

		log::trace!("Setting commands successful!");
		Ok(())
	}

	pub async fn handle_self(self, bot: Bot, message: Message, database: Arc<DatabaseInterface>) -> CommandResult {
		log::trace!(
			"Handling command in {:?} with id {:?} and contents {:?}",
			&message.chat.id,
			&message.id,
			self
		);

		let result1 = match self {
			Command::Start => start::handler(&bot, &message).await,
			Command::Help(ref target) => match target.as_str() {
				"" => help::handler_all(&bot, &message).await,
				_ => help::handler_specific(&bot, &message, target).await,
			},
			Command::Fortune => fortune::handler(&bot, &message).await,
			Command::Echo(ref text) => echo::handler(&bot, &message, text).await,
			Command::WhoAmI => whoami::handler(&bot, &message, &database).await,
			Command::Answer(_) => answer::handler(&bot, &message).await,
			Command::Reminder(ref args) => reminder::handler(&bot, &message, args).await,
			Command::Dog => dog::handler(&bot, &message).await,
			Command::Cat => cat::handler(&bot, &message).await,
      		Command::Roll(ref roll) => roll::handler(&bot, &message, roll).await,
			Command::Diario(ref args) => diario::handler(&bot, &message, args, &database).await,
			Command::Matchmaking(ref args) => matchmaking::handler(&bot, &message, args, &database).await,
		};

		let result2 = match result1.as_ref() {
			Ok(_) => return Ok(()),
			Err(e1) => self.handle_error(&bot, &message, e1).await
		};

		let e1 = result1.unwrap_err();

		match result2 {
			Ok(_) => return Ok(()),
			Err(e2) => self.handle_fatal(&bot, &message, &e1, &e2).await
		}?;

		Ok(())
	}

	pub async fn handle_unknown(bot: Bot, message: Message) -> CommandResult {
		log::debug!("Received an unknown command or an invalid syntax.");

		let _reply = bot
			.send_message(message.chat.id, "⚠️ Comando sconosciuto o sintassi non valida.")
			.reply_to_message_id(message.id)
			.await
			.context("Non è stato possibile inviare la risposta.")?;

		Ok(())
	}

	async fn handle_error(&self, bot: &Bot, message: &Message, error: &Error) -> CommandResult {
		log::debug!(
			"Command message in {:?} with id {:?} and contents {:?} errored out with `{:?}`",
			&message.chat.id,
			&message.id,
			self,
			error,
		);

		let _reply = bot
			.send_message(message.chat.id, format!("⚠️ {error}"))
			.reply_to_message_id(message.id)
			.await
			.context("Non è stato possibile inviare la risposta.")?;

		Ok(())
	}

	async fn handle_fatal(&self, _bot: &Bot, message: &Message, error1: &Error, error2: &Error) -> CommandResult {
		log::error!(
			"Command message in {:?} with id {:?} and contents {:?} errored out with `{:?}`, and it was impossible to handle the error because of `{:?}`",
			&message.chat.id,
			&message.id,
			self,
			error1,
			error2,
		);

		Ok(())
	}
}

type CommandResult = Result<()>;
