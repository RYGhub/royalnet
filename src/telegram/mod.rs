use anyhow::Error;
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
