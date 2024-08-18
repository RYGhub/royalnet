use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use super::matchmaking_events::MatchmakingEvent;
use super::super::schema::matchmaking_messages_telegram;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(MatchmakingEvent, foreign_key = matchmaking_id))]
#[diesel(table_name = matchmaking_messages_telegram)]
#[diesel(primary_key(matchmaking_id, telegram_chat_id, telegram_message_id))]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingMessageTelegram {
	pub matchmaking_id: i32,
	pub telegram_chat_id: i64,
	pub telegram_message_id: i32,
}
