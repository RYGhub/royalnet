use anyhow::{Context, Result};
use teloxide::dispatching::HandlerExt;

pub(crate) mod database;
mod telegram;

#[tokio::main]
async fn main() -> Result<()> {
    // Logging setup
    {
        pretty_env_logger::init();
        log::info!("Logging initialized successfully!");
    }
    // Telegram setup
    {
        log::trace!("Setting up Telegram bot...");
        let mut dispatcher = telegram::dispatcher();
        dispatcher.dispatch().await
    }

    Ok(())
}
