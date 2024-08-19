use std::time::Duration;

use tokio::time::sleep;

use crate::utils::anyhow_result::AnyResult;

#[allow(dead_code)]
pub trait RoyalnetService {
	async fn run(&mut self) -> AnyResult<()>;
	
	async fn run_loop(&mut self) {
		let mut backoff = Duration::new(1, 0);
		
		loop {
			let result = self.run().await;
			
			match result {
				Err(e) => {
					log::error!("Service exited with error: {e:?}.")
				}
				_ => {
					log::debug!("Service exited successfully!")
				}
			}
			
			let backoff_secs = backoff.as_secs();
			
			log::debug!("Backing off for {backoff_secs} seconds before restarting...");
			sleep(backoff).await;
			
			log::trace!("Doubling backoff value...");
			backoff *= 2;
			
			log::trace!("Backoff value is now {backoff_secs} seconds.");
		}
	}
}

#[cfg(feature = "service_telegram")]
pub mod telegram;

#[cfg(feature = "service_brooch")]
pub mod brooch;
