use std::convert::Infallible;
use teloxide::Bot;
use super::RoyalnetService;

mod config;
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
}

impl RoyalnetService for BotService {
	async fn run(mut self) -> anyhow::Result<Infallible> {
		log::info!("Starting Telegram service...");

		log::debug!("Setting bot commands...");
		commands::Command::set_commands(&mut self.bot).await?;

		log::debug!("Starting Telegram dispatcher...");
		commands::dispatcher(self.bot).dispatch().await;

		log::error!("Telegram dispatcher has exited, bailing out...");
		anyhow::bail!("Telegram dispatcher has exited.")
	}
}
