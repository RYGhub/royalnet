use anyhow::Context;
use diesel::{Identifiable, Insertable, PgConnection, Queryable, Selectable};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::ToSql;
use crate::utils::result::AnyResult;
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

		let addition = MatchmakingEventAddition {
			text: text.to_string(),
			starts_at: starts_at.naive_local(),
		};

		insert_into(matchmaking_events::table)
			.values(&addition)
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
}

#[repr(transparent)]
#[derive(Debug, Clone, PartialEq)]
pub struct MatchmakingId(pub(crate) i32);

impl From<i32> for MatchmakingId {
	fn from(value: i32) -> Self {
		Self(value)
	}
}

impl From<MatchmakingId> for i32 {
	fn from(value: MatchmakingId) -> Self {
		value.0
	}
}

impl ToSql<i32, Pg> for MatchmakingId {
	fn to_sql(&self, out: &mut diesel::serialize::Output<Pg>) -> diesel::serialize::Result {
		self.0
			.to_sql(out)
	}
}

impl FromSql<i32, Pg> for MatchmakingId {
	fn from_sql(raw: PgValue) -> diesel::deserialize::Result<Self> {
		i32::from_sql(raw)
			.map(Self)
	}
}
