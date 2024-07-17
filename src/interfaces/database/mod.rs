use diesel::{Connection, ConnectionResult, PgConnection};

pub mod schema;
pub mod models;

pub fn connect(database_url: &str) -> ConnectionResult<PgConnection> {
	PgConnection::establish(database_url)
}
