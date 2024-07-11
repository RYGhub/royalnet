use std::convert::Infallible;
use anyhow::Result;

pub mod telegram;

pub trait RoyalnetService {
	async fn run_royalnet(self) -> Result<Infallible>;
}

impl RoyalnetService for teloxide::dispatching::Dispatcher<teloxide::Bot, anyhow::Error, teloxide::dispatching::DefaultKey> {
	async fn run_royalnet(mut self) -> Result<Infallible> {
		log::info!("Starting Telegram service...");
		self.dispatch().await;

		log::error!("Telegram dispatcher has exited, bailing out...");
		anyhow::bail!("Telegram dispatcher has exited.")
	}
}
