use anyhow::anyhow;
use diesel::{Connection, ConnectionResult, PgConnection};
use diesel::migration::MigrationVersion;
use diesel_migrations::{embed_migrations, EmbeddedMigrations, MigrationHarness};
use crate::utils::result::AnyResult;

pub mod schema;
pub mod models;

pub fn connect(database_url: &str) -> ConnectionResult<PgConnection> {
	PgConnection::establish(database_url)
}

const MIGRATIONS: EmbeddedMigrations = embed_migrations!();

pub fn migrate(database: &mut PgConnection) -> AnyResult<Vec<MigrationVersion>> {
	database.run_pending_migrations(MIGRATIONS)
		.map_err(|e| anyhow!("Failed to run pending migrations: {e:?}"))
}