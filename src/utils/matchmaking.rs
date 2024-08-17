use anyhow::Context;
use diesel::PgConnection;
use crate::interfaces::database::models::{MatchmakingEvent, MatchmakingEventAddition};

impl MatchmakingEvent {
	pub fn create(database: &mut PgConnection, matchmaking_text: &str, matchmaking_starts_at: &chrono::DateTime<chrono::Local>) -> anyhow::Result<Self> {
		use diesel::prelude::*;
		use diesel::dsl::*;
		use crate::interfaces::database::schema::matchmaking_events::dsl::*;

		insert_into(matchmaking_events)
			.values(&MatchmakingEventAddition {
				text: matchmaking_text.to_string(),
				starts_at: matchmaking_starts_at.naive_local(),
			})
			.get_result::<MatchmakingEvent>(database)
			.context("Non è stato possibile aggiungere il matchmaking al database RYG.")
	}

	pub fn get(database: &mut PgConnection, matchmaking_id: i32) -> anyhow::Result<MatchmakingEvent> {
		use diesel::prelude::*;
		use crate::interfaces::database::schema::matchmaking_events::dsl::*;

		matchmaking_events
			.filter(id.eq(matchmaking_id))
			.get_result::<MatchmakingEvent>(database)
			.context("Non è stato possibile recuperare il matchmaking dal database RYG.")
	}
}
