// See the following link for an example of how to use this file:
// https://github.com/teloxide/teloxide/blob/master/crates/teloxide/examples/dispatching_features.rs

use std::sync::Arc;

use anyhow::{Context, Error};
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message, ReplyParameters};
use teloxide::utils::command::BotCommands;
use teloxide::Bot;

use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::utils::anyhow_result::AnyResult;
use crate::utils::italian::countable_noun_suffix;

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


type CommandResult = AnyResult<()>;

#[derive(Debug, Clone, PartialEq, Eq, BotCommands)]
#[command(rename_rule = "lowercase")]
pub enum Command {
	#[command(description = "Invia messaggio di introduzione.")]
	Start,
	#[command(
		description = "Visualizza l'elenco dei comandi disponibili, o mostra informazioni su uno specifico comando."
	)]
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
	/// Update the [commands menu](https://core.telegram.org/bots/features#commands) of the bot.
	pub async fn set_commands(bot: &mut Bot) -> AnyResult<()> {
		log::debug!("Setting bot commands...");
		
		log::trace!("Determining bot commands...");
		let commands = Self::bot_commands();
		
		log::trace!("Setting commands: {commands:#?}");
		bot.set_my_commands(commands).await
			.context("Non è stato possibile aggiornare la lista comandi del bot.")?;
		
		log::trace!("Setting commands successful!");
		Ok(())
	}
	
	pub async fn handle_self(self, bot: Bot, message: Message, database: Arc<DatabaseInterface>) -> CommandResult {
		log::debug!("Handling command...");
		
		log::trace!(
			"Handling {:?} in {:?} with {:?}...",
			self,
			&message.chat.id,
			&message.id,
		);
		
		// FIXME: Quick hack to fix single thread
		log::trace!("Spawning task for future...");
		let _task = tokio::spawn(async move {
			log::trace!("Delegating command handling to handler...");
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
			
			log::trace!("Delegating error handling to error handler...");
			let result2 = match result1.as_ref() {
				Ok(_) => return,
				Err(e1) => self.handle_error_command(&bot, &message, e1).await
			};
			
			let e1 = result1.unwrap_err();
			
			log::trace!("Delegating fatal error handling to fatal error handler...");
			let _result3 = match result2 {
				Ok(_) => return,
				Err(e2) => self.handle_fatal(&bot, &message, &e1, &e2).await
			};
			
			log::trace!("Successfully handled command!");
		});
		
		log::trace!("Successfully spawned task!");
		Ok(())
	}
	
	pub async fn handle_malformed_simple(bot: Bot, message: Message, expected: usize, found: usize) -> CommandResult {
		log::debug!("Received a malformed command: {:?}", message.text());
		
		log::trace!("Sending error message...");
		let text = format!(
			"⚠️ Il comando si aspetta {} argoment{}, ma ne ha ricevut{} solo {}.",
			expected,
			countable_noun_suffix(expected, "o", "i"),
			countable_noun_suffix(found, "o", "i"),
			found,
		);
		let _reply = bot
			.send_message(message.chat.id, text)
			.reply_parameters(ReplyParameters::new(message.id))
			.await
			.context("Non è stato possibile inviare il messaggio di errore.")?;
		
		log::trace!("Successfully handled malformed command!");
		Ok(())
	}
	
	pub async fn handle_malformed_complex(bot: Bot, message: Message) -> CommandResult {
		log::debug!("Received a malformed command: {:?}", message.text());
		
		log::trace!("Sending error message...");
		let text = "⚠️ Il comando si aspetta una sintassi diversa da quella che ha ricevuto.";
		let _reply = bot
			.send_message(message.chat.id, text)
			.reply_parameters(ReplyParameters::new(message.id))
			.await
			.context("Non è stato possibile inviare il messaggio di errore.")?;
		
		log::trace!("Successfully handled malformed command!");
		Ok(())
	}
	
	pub async fn handle_unknown(bot: Bot, message: Message) -> CommandResult {
		log::debug!("Received an unknown command: {:?}", message.text());
		
		log::trace!("Sending error message...");
		let text = "⚠️ Il comando specificato non esiste.";
		let _reply = bot
			.send_message(message.chat.id, text)
			.reply_parameters(ReplyParameters::new(message.id))
			.await
			.context("Non è stato possibile inviare il messaggio di errore.")?;
		
		log::trace!("Successfully handled unknown command!");
		Ok(())
	}
	
	pub async fn handle_error_parse(bot: &Bot, message: &Message, error: &Error) -> CommandResult {
		log::debug!("Encountered a parsing error while parsing: {:?}", message.text());
		
		log::trace!("Sending error message...");
		let text = format!("⚠️ {error}");
		let _reply = bot
			.send_message(message.chat.id, text)
			.reply_parameters(ReplyParameters::new(message.id))
			.await
			.context("Non è stato possibile inviare il messaggio di errore.")?;
		
		log::trace!("Successfully handled malparsed command!");
		Ok(())
	}
	
	pub async fn handle_error_command(&self, bot: &Bot, message: &Message, error: &Error) -> CommandResult {
		log::debug!(
			"Command message in {:?} with id {:?} and contents {:?} errored out with `{:?}`",
			&message.chat.id,
			&message.id,
			self,
			error,
		);
		
		log::trace!("Sending error message...");
		let text = format!("⚠️ {error}");
		let _reply = bot
			.send_message(message.chat.id, text)
			.reply_parameters(ReplyParameters::new(message.id))
			.await
			.context("Non è stato possibile inviare il messaggio di errore.")?;
		
		log::trace!("Successfully handled errored command!");
		Ok(())
	}
	
	pub async fn handle_fatal(&self, _bot: &Bot, message: &Message, error1: &Error, error2: &Error) -> CommandResult {
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
