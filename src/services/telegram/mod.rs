use std::sync::Arc;

use anyhow::Context;
use commands::Command;
use dependencies::interface_database::DatabaseInterface;
use keyboard_callbacks::KeyboardCallback;
use teloxide::dispatching::DefaultKey;
use teloxide::dptree::entry;
use teloxide::prelude::*;
use teloxide::types::{Me, ParseMode};
use teloxide::utils::command::{BotCommands, ParseError};

use crate::utils::anyhow_result::AnyResult;
use crate::utils::telegram_string::TelegramEscape;

use super::RoyalnetService;

mod commands;
mod dependencies;
mod keyboard_callbacks;
pub(crate) mod utils;

#[derive(Debug, Clone)]
pub struct TelegramService {
	database_url: String,
	bot: Bot,
	me: Me,
	notification_chat_id: Option<ChatId>,
}

impl TelegramService {
	pub async fn new(database_url: String, token: String, notification_chat_id: Option<ChatId>) -> AnyResult<Self> {
		log::info!("Initializing a new Telegram service...");
		
		let bot = Bot::new(token);
		
		log::trace!("Using bot: {bot:#?}");
		
		let me = Self::get_me(&bot)
			.await?;
		
		log::trace!("Using self details: {me:#?}");
		
		let service = Self {
			database_url,
			bot,
			me,
			notification_chat_id,
		};
		
		log::trace!("Created service: {service:#?}");
		
		Ok(service)
	}
	
	async fn get_me(bot: &Bot) -> AnyResult<Me> {
		log::debug!("Getting self details...");
		bot.get_me().await
			.context("Recupero dettagli sul bot non riuscito.")
	}
	
	async fn send_start_notification(&self) -> AnyResult<Message> {
		log::debug!("Sending start notification...");
		
		let notification_chat_id = self.notification_chat_id
			.context("La chat di notifica non è abilitata.")?;
		
		let version = crate::utils::version::VERSION
			.escape_telegram_html();
		
		let username = self.me.username
			.as_ref()
			.unwrap()
			.escape_telegram_html();
		
		let id = self.me.user.id
			.to_string()
			.escape_telegram_html();
		
		let text = format!(
			"💠 <b>Servizio Telegram avviato</b>\n\
			\n\
			Royalnet <a href='https://github.com/RYGhub/royalnet/releases/tag/v{version}'>v{version}</a>\n\
			\n\
			@{username} [<code>{id}</code>]"
		);
		
		log::trace!("Sending start notification message...");
		let msg = self.bot.send_message(notification_chat_id, text)
			.parse_mode(ParseMode::Html)
			.await
			.context("Invio della notifica di avvio non riuscito.")?;
		
		log::trace!("Successfully sent start notification message!");
		Ok(msg)
	}
	
	async fn set_commands(&mut self) -> AnyResult<()> {
		log::debug!("Setting self commands...");
		Command::set_commands(&mut self.bot).await
			.context("Aggiornamento dei comandi del bot non riuscito.")
	}
	
	async fn handle_message(bot: Bot, me: Me, message: Message, database: Arc<DatabaseInterface>) -> AnyResult<()> {
		log::debug!("Handling message: {message:#?}");
		
		log::trace!("Accessing message text...");
		let text = match message.text() {
			None => {
				log::trace!("Message has no text; skipping it.");
				return Ok(())
			}
			Some(text) => {
				log::trace!("Message has text: {text:?}");
				text
			}
		};
		
		log::trace!("Checking if message is actually a command...");
		if !text.starts_with("/") {
			log::trace!("Message is not a command.");
			return Ok(())
		}
		
		log::trace!("Retrieving bot's username...");
		let username = me.username();
		
		log::trace!("Parsing message text {text:?} as {username:?}...");
		let command = match Command::parse(text, username) {
			Ok(command) => {
				log::trace!("Message text parsed successfully as: {command:?}");
				command
			}
			Err(ParseError::WrongBotName(receiver)) => {
				log::debug!("Message is meant to be sent to {receiver:?}, while I'm running as {username:?}; skipping it.");
				return Ok(());
			}
			Err(ParseError::TooFewArguments { expected, found, .. }) |
			Err(ParseError::TooManyArguments { expected, found, .. }) => {
				log::debug!("Message text is a command with {found} arguments, but the command expected {expected}; handling as a malformed command.");
				Command::handle_malformed_simple(bot, message, expected, found).await
					.context("Impossibile gestire comando malformato semplice.")?;
				return Ok(());
			}
			Err(ParseError::IncorrectFormat(e)) => {
				log::debug!("Message text is a command with a custom format, but the parser returned the error {e:?}; handling as a malformed command.");
				let error = anyhow::format_err!(e);
				Command::handle_malformed_complex(&bot, &message, &error).await
					.context("Impossibile gestire comando malformato complesso.")?;
				return Ok(());
			}
			Err(ParseError::UnknownCommand(command)) => {
				log::debug!("Message text is command not present in the commands list {command:?}; handling it as an unknown command.");
				Command::handle_unknown(bot, message).await
					.context("Impossibile gestire comando sconosciuto.")?;
				return Ok(());
			}
			Err(ParseError::Custom(e)) => {
				log::debug!("Message text is a command, but the parser raised custom error {e:?}; handling it as a custom error.");
				let error = anyhow::format_err!(e);
				Command::handle_error_parse(&bot, &message, &error).await
					.context("Impossibile gestire comando con errore di parsing.")?;
				return Ok(());
			}
		};
		
		command.handle_self(bot, message, database).await
			.context("Impossibile gestire errore restituito dal comando.")?;
		
		Ok(())
	}
	
	fn dispatcher(&mut self) -> Dispatcher<Bot, anyhow::Error, DefaultKey> {
		log::debug!("Building dispatcher...");
		
		let bot_name = self.me.user.username.as_ref().unwrap();
		log::trace!("Bot username is: @{bot_name:?}");
		
		let database = Arc::new(DatabaseInterface::new(self.database_url.clone()));
		
		log::trace!("Building dispatcher...");
		Dispatcher::builder(
			self.bot.clone(),
			// When an update is received
			entry()
				// Messages
				.branch(Update::filter_message()
					// Handle incoming messages
					.endpoint(Self::handle_message)
				)
				// Inline keyboard
				.branch(Update::filter_callback_query()
					// Known callbacks
					.branch(entry()
						// Only process queries that match
						.filter_map(move |query: CallbackQuery| query.data
							// Parse the data string as a KeyboardCallback
							.and_then(|data| data.parse::<KeyboardCallback>().ok())
						)
						.endpoint(KeyboardCallback::handle_self)
					)
					.endpoint(KeyboardCallback::handle_unknown)
				),
		)
			.dependencies(
				dptree::deps![
					database
				]
			)
			.default_handler(|upd| async move {
				log::trace!("Unhandled update: {:?}", upd);
			})
			.build()
	}
	
	async fn dispatch(&mut self) -> AnyResult<()> {
		log::debug!("Starting Telegram dispatcher...");
		self.dispatcher().dispatch().await;
		
		anyhow::bail!("Telegram dispatcher has exited unexpectedly.")
	}
}

impl RoyalnetService for TelegramService {
	async fn run(&mut self) -> AnyResult<()> {
		log::info!("Starting Telegram service...");
		
		let _ = self.set_commands()
			.await;
		
		let _ = self.send_start_notification()
			.await;
		
		self.dispatch()
			.await
	}
}
