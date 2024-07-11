use std::convert::Infallible;
use teloxide::Bot;
use anyhow::{Context, Result};
use teloxide::requests::Requester;
use super::RoyalnetService;

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

	async fn send_start_notification(&mut self) -> Result<()> {
		let chat_id = config::TELEGRAM_NOTIFICATION_CHATID()
			.context("Variabile d'ambiente TELEGRAM_NOTIFICATION_CHATID mancante.")?;

		let text = format!(
			"💠 Servizio Telegram avviato\n\
				Royalnet v{}",
			crate::utils::version::VERSION,
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

		log::debug!("Setting bot commands...");
		match commands::Command::set_commands(&mut self.bot).await {
			Err(e) => log::warn!("Failed to set bot commands: {e}"),
			_ => log::trace!("Bot commands set successfully!"),
		}

		log::debug!("Sending start notification...");
		match self.send_start_notification().await {
			Err(e) => log::warn!("Failed to send start notification: {e}"),
			_ => log::trace!("Start notification sent successfully!"),
		}

		log::debug!("Starting Telegram dispatcher...");
		commands::dispatcher(self.bot).dispatch().await;

		log::error!("Telegram dispatcher has exited, bailing out...");
		anyhow::bail!("Telegram dispatcher has exited.")
	}
}
