use std::sync::Arc;

use anyhow::Context;
use regex::Regex;
use teloxide::dispatching::DefaultKey;
use teloxide::dptree::entry;
use teloxide::prelude::*;
use teloxide::types::{Me, ParseMode};

use commands::Command;
use dependencies::interface_database::DatabaseInterface;
use keyboard_callbacks::KeyboardCallback;

use crate::utils::anyhow_result::{AnyError, AnyResult};
use crate::utils::telegram_string::TelegramEscape;

use super::RoyalnetService;

mod commands;
mod dependencies;
mod keyboard_callbacks;
mod utils;

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
	
	fn dispatcher(&mut self) -> Dispatcher<Bot, AnyError, DefaultKey> {
		log::debug!("Building dispatcher...");
		
		let bot_name = self.me.user.username.as_ref().unwrap();
		log::trace!("Bot username is: @{bot_name:?}");
		
		log::trace!("Determining pseudo-command regex...");
		let regex = Regex::new(&format!(r"^/[a-z0-9_]+(?:@{bot_name})?(?:\s+.*)?$")).unwrap();
		log::trace!("Pseudo-command regex is: {regex:?}");
		
		let database = Arc::new(DatabaseInterface::new(self.database_url.clone()));
		
		log::trace!("Building dispatcher...");
		Dispatcher::builder(
			self.bot.clone(),
			// When an update is received
			entry()
				// Messages
				.branch(Update::filter_message()
					// Pseudo-commands
					.branch(entry()
						// Only process commands matching the pseudo-command regex
						.filter(move |message: Message| -> bool {
							message
								.text()
								.is_some_and(|text| regex.is_match(text))
						})
						// Commands
						.branch(entry()
							// Only process commands matching a valid command, and parse their arguments
							.filter_command::<Command>()
							// Delegate handling
							.endpoint(Command::handle_self)
						)
						// No valid command was found
						.endpoint(Command::handle_unknown)
					)
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
