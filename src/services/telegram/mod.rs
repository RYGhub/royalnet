use std::convert::Infallible;
use teloxide::{Bot, dptree};
use anyhow::{Context, Error, Result};
use regex::Regex;
use teloxide::dispatching::{DefaultKey, Dispatcher, HandlerExt, UpdateFilterExt};
use teloxide::dptree::entry;
use teloxide::requests::Requester;
use teloxide::types::{Me, Message, Update};
use super::RoyalnetService;

#[allow(clippy::needless_pub_self)]
pub(self) mod config;
mod commands;

pub struct BotService {
	pub bot: Bot
}

impl BotService {
	pub fn from_config() -> Self {
		Self {
			bot: Bot::new(config::TELEGRAM_BOT_TOKEN())
		}
	}

	async fn send_start_notification(&mut self, me: &Me) -> Result<()> {
		let chat_id = config::TELEGRAM_NOTIFICATION_CHATID()
			.context("Variabile d'ambiente TELEGRAM_NOTIFICATION_CHATID mancante.")?;

		let version = crate::utils::version::VERSION;
		let username = &me.username.as_ref().unwrap();
		let id = &me.user.id;

		let text = format!(
			"💠 Servizio Telegram avviato\n\
				Royalnet v{version}\n\
				@{username} ({id})",
		);

		self.bot.send_message(chat_id, text)
			.await
			.context("Invio della notifica di avvio non riuscito.")?;

		Ok(())
	}
}

impl RoyalnetService for BotService {
	async fn run(mut self) -> Result<Infallible> {
		log::info!("Starting Telegram service...");

		log::debug!("Getting bot information...");
		let me = self.bot.get_me().await
			.context("Failed to get information about self")?;

		log::debug!("Setting bot commands...");
		match commands::Command::set_commands(&mut self.bot).await {
			Err(e) => log::warn!("Failed to set bot commands: {e}"),
			_ => log::trace!("Bot commands set successfully!"),
		}

		log::debug!("Sending start notification...");
		match self.send_start_notification(&me).await {
			Err(e) => log::warn!("Failed to send start notification: {e}"),
			_ => log::trace!("Start notification sent successfully!"),
		}

		log::debug!("Starting Telegram dispatcher...");
		dispatcher(self.bot, me).dispatch().await;

		log::error!("Telegram dispatcher has exited, bailing out...");
		anyhow::bail!("Telegram dispatcher has exited.")
	}
}

fn dispatcher(bot: Bot, me: Me) -> Dispatcher<Bot, Error, DefaultKey> {
	let bot_name = me.user.username.unwrap();
	log::trace!("Bot name is: {bot_name:?}");

	let regex = Regex::new(&format!(r"^/[a-z0-9_]+(?:@{bot_name})?(?:\s+.*)?$")).unwrap();
	log::trace!("Pseudo-command regex is: {regex:?}");

	log::trace!("Building dispatcher...");
	Dispatcher::builder(
		bot,
		Update::filter_message()
			.branch(entry()
				.filter(move |message: Message| -> bool {
					message.text().is_some_and(|text| regex.is_match(text))
				})
				.branch(
					entry()
						.filter_command::<commands::Command>()
						.endpoint(commands::Command::handle)
				)
				.endpoint(commands::unknown_command)
			)
	)
		.dependencies(
			dptree::deps![]  // No deps needed at the moment.
		)
		.build()
}
