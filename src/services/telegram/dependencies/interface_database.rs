use anyhow::Context;
use diesel::PgConnection;
use crate::utils::anyhow_result::AnyResult;

#[derive(Debug, Clone)]
pub struct DatabaseInterface {
	database_url: String,
}

impl DatabaseInterface {
	pub fn new(database_url: String) -> Self {
		Self { database_url }
	}

	pub fn connect(&self) -> AnyResult<PgConnection> {
		crate::interfaces::database::connect(&self.database_url)
			.context("Impossibile connettersi al database RYG.")
	}
}
