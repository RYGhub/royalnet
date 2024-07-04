use diesel::{Connection, ConnectionResult, PgConnection};

pub(self) mod config;
pub mod schema;
pub mod models;

pub fn connect() -> ConnectionResult<PgConnection> {
	PgConnection::establish(config::DATABASE_URL())
}
