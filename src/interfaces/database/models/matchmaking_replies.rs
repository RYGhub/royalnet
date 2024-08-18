use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

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
	pub matchmaking_id: i32,
	pub user_id: i32,
	pub choice: MatchmakingChoice,
	pub late_mins: i32,
}
