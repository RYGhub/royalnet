use anyhow::{Result};
use crate::telegram::DispatchWithResult;

pub(crate) mod database;
mod telegram;

#[tokio::main]
async fn main() -> Result<()> {
    // Logging setup
    pretty_env_logger::init();
    log::debug!("Logging initialized successfully!");

    // Telegram setup
    log::trace!("Setting up Telegram bot dispatcher...");
    let mut telegram_dispatcher = telegram::dispatcher();
    let telegram_awaitable = telegram_dispatcher.dispatch_with_result();

    // Run all services concurrently
    log::info!("Starting services...");
    tokio::try_join![
        telegram_awaitable,
    ];

    // This should never happen, but just in case...
    log::error!("A service has exited, bailing out...");
    anyhow::bail!("A service has exited.")
}
