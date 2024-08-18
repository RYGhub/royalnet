use diesel::{Connection, ConnectionResult, PgConnection};

pub fn connect(database_url: &str) -> ConnectionResult<PgConnection> {
	PgConnection::establish(database_url)
}
