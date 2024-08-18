use anyhow::Context;
use diesel::{AsExpression, FromSqlRow, Identifiable, Insertable, PgConnection, Queryable, QueryId, Selectable};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::ToSql;
use crate::newtype_sql;
use crate::utils::anyhow_result::AnyResult;
use super::super::schema::matchmaking_events;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = matchmaking_events)]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingEvent {
	pub id: MatchmakingId,
	pub text: String,
	pub starts_at: chrono::NaiveDateTime,
}

impl MatchmakingEvent {
	/// Create a new [MatchmakingEvent].
	pub fn create(database: &mut PgConnection, text: &str, starts_at: &chrono::DateTime<chrono::Local>) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;

		insert_into(matchmaking_events::table)
			.values(&(
				matchmaking_events::text.eq(text),
				matchmaking_events::starts_at.eq(starts_at.naive_utc()),
			))
			.get_result::<Self>(database)
			.context("Non è stato possibile aggiungere il matchmaking al database RYG.")
	}

	/// Retrieve a [MatchmakingEvent] from the database, given its [MatchmakingId].
	pub fn get(database: &mut PgConnection, matchmaking_id: MatchmakingId) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;

		matchmaking_events::table
			.filter(matchmaking_events::id.eq(matchmaking_id.0))
			.get_result::<Self>(database)
			.context("Non è stato possibile recuperare il matchmaking dal database RYG.")
	}

	pub fn has_started(&self) -> bool {
		self.starts_at.lt(&chrono::Local::now().naive_utc())
	}
}

newtype_sql!(pub MatchmakingId: diesel::sql_types::Int4 as i32);

impl MatchmakingId {
	pub fn callback_data(&self, data: &str) -> String {
		format!("matchmaking:{}:{}", &self.0, data)
	}
}
