use anyhow::Result;
use services::telegram;
use crate::services::RoyalnetService;

pub(crate) mod database;
pub(crate) mod utils;
mod services;


#[tokio::main]
async fn main() -> Result<()> {
    // Logging setup
    pretty_env_logger::init();
    log::debug!("Logging initialized successfully!");

    // Telegram setup
    log::trace!("Setting up Telegram bot service...");
    let telegram = telegram::init();

    // Run all services concurrently
    log::info!("Starting services...");
    let result = tokio::try_join![
        telegram.run_royalnet(),
    ];

    // This should never happen, but just in case...
    match result {
        Err(error) => {
            log::error!("A service has exited with an error, bailing out: {error:?}");
            anyhow::bail!("A service has exited with an error.")
        },
        _ => {
            log::error!("All service have exited successfully, bailing out...");
            anyhow::bail!("All service have exited successfully.")
        }
    }
}
