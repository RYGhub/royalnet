use anyhow::anyhow;
use diesel::migration::MigrationVersion;
use diesel::PgConnection;
use diesel_migrations::{embed_migrations, EmbeddedMigrations, MigrationHarness};
use crate::utils::result::AnyResult;

const MIGRATIONS: EmbeddedMigrations = embed_migrations!();

pub fn migrate(database: &mut PgConnection) -> AnyResult<Vec<MigrationVersion>> {
	database.run_pending_migrations(MIGRATIONS)
		.map_err(|e| anyhow!("Failed to run pending migrations: {e:?}"))
}
