use std::convert::Infallible;
use anyhow::{Error, Result};
use teloxide::Bot;
use teloxide::dispatching::{DefaultKey, Dispatcher};

mod config;
mod commands;

pub fn dispatcher() -> Dispatcher<Bot, Error, DefaultKey> {
	commands::dispatcher(
		Bot::new(
			config::TELEGRAM_BOT_TOKEN()
		)
	)
}

pub trait DispatchWithResult {
	async fn dispatch_with_result(&mut self) -> Result<Infallible>;
}

impl DispatchWithResult for Dispatcher<Bot, Error, DefaultKey> {
	async fn dispatch_with_result(&mut self) -> Result<Infallible> {
		log::info!("Starting Telegram dispatcher...");
		self.dispatch().await;
		log::error!("Telegram dispatcher has exited, bailing out...");

		anyhow::bail!("Telegram dispatcher has exited.")
	}
}