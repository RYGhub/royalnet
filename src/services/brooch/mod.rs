use std::convert::Infallible;
use std::future::Future;
use crate::services::RoyalnetService;
use crate::stratz::query_guild_matches;

mod config;

pub struct BroochService {}

impl RoyalnetService for BroochService {
	async fn run(self) -> anyhow::Result<Infallible> {
		let client = reqwest::Client::new();

		match query_guild_matches(client, config::BROOCH_WATCHED_GUILD_ID()) {

		}
	}
}