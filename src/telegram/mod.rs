use teloxide::Bot;

mod config;

pub fn connect() -> Bot {
	Bot::new(config::TELEGRAM_BOT_TOKEN())
}
