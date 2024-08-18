use crate::instance::RoyalnetInstance;

mod instance;
mod interfaces;
mod services;
pub(crate) mod utils;

#[tokio::main]
async fn main() {
    // Logging setup
    pretty_env_logger::init();
    log::debug!("Logging initialized successfully!");

    // Create instance
    let instance = RoyalnetInstance::new().await;

    log::trace!("Starting {instance:?}!");
    instance.run().await;

    log::error!("No services configured.");
}
