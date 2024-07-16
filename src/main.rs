use anyhow::Result;
use crate::services::RoyalnetService;

pub(crate) mod database;
pub(crate) mod utils;
mod services;
mod stratz;

#[tokio::main]
async fn main() -> Result<()> {
    // Logging setup
    pretty_env_logger::init();
    log::debug!("Logging initialized successfully!");

    // Telegram setup
    log::trace!("Setting up Telegram bot service...");
    let telegram = services::telegram::BotService::from_config();

    // Brooch setup
    log::trace!("Setting up Brooch service...");
    let brooch = services::brooch::BroochService::from_config();

    // Run all services concurrently
    log::info!("Starting services...");
    let result = tokio::try_join![
        telegram.run(),
        brooch.run(),
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
