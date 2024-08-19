use std::ops::Add;

use anyhow::Context;
use diesel::{Associations, Identifiable, Insertable, PgConnection, Queryable, Selectable};
use diesel::pg::Pg;

use crate::interfaces::database::models::{MatchmakingId, RoyalnetUserId, TelegramUser};
use crate::utils::anyhow_result::AnyResult;

use super::matchmaking_choice::MatchmakingChoice;
use super::matchmaking_events::MatchmakingEvent;
use super::super::schema::matchmaking_replies;
use super::users::RoyalnetUser;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(MatchmakingEvent, foreign_key = matchmaking_id))]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = matchmaking_replies)]
#[diesel(primary_key(matchmaking_id, user_id))]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingReply {
	pub matchmaking_id: MatchmakingId,
	pub user_id: RoyalnetUserId,
	pub choice: MatchmakingChoice,
	pub late_mins: i32,
}

impl MatchmakingReply {
	pub fn get_all_telegram(database: &mut PgConnection, matchmaking_id: MatchmakingId) -> AnyResult<Vec<(Self, RoyalnetUser, TelegramUser)>> {
		use crate::interfaces::database::query_prelude::*;
		
		matchmaking_replies::table
			.filter(matchmaking_replies::matchmaking_id.eq(matchmaking_id))
			.inner_join(users::table.on(matchmaking_replies::user_id.eq(users::id)))
			.inner_join(telegram::table.on(users::id.eq(telegram::user_id)))
			.get_results::<(Self, RoyalnetUser, TelegramUser)>(database)
			.context("Non è stato possibile recuperare le risposte al matchmaking dal database RYG.")
	}
	
	pub fn set(database: &mut PgConnection, matchmaking_id: MatchmakingId, user_id: RoyalnetUserId, choice: MatchmakingChoice) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;
		
		insert_into(matchmaking_replies::table)
			.values(&Self {
				matchmaking_id,
				user_id,
				choice,
				late_mins: 0,
			})
			.on_conflict(on_constraint("matchmaking_replies_pkey"))
			.do_update()
			.set((
				matchmaking_replies::choice.eq(choice),
				matchmaking_replies::late_mins.eq(0),
			))
			.get_result::<Self>(database)
			.context("Non è stato possibile inserire la risposta al matchmaking nel database RYG.")
	}
	
	pub fn add_late_minutes(database: &mut PgConnection, matchmaking_id: MatchmakingId, user_id: RoyalnetUserId, increase_by: i32) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;
		
		insert_into(matchmaking_replies::table)
			.values(&Self {
				matchmaking_id,
				user_id,
				choice: MatchmakingChoice::Late,
				late_mins: increase_by,
			})
			.on_conflict(on_constraint("matchmaking_replies_pkey"))
			.do_update()
			.set((
				matchmaking_replies::choice.eq(MatchmakingChoice::Late),
				matchmaking_replies::late_mins.eq(matchmaking_replies::late_mins.add(increase_by)),
			))
			.get_result::<Self>(database)
			.context("Non è stato possibile aumentare il ritardo nella risposta nel database RYG.")
	}
}
