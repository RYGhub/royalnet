use std::io::Write;
use diesel::{Identifiable, Insertable, Queryable, Selectable, Associations, FromSqlRow, AsExpression};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::{IsNull, ToSql};
use super::schema::*;


#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = users)]
#[diesel(check_for_backend(Pg))]
pub struct RoyalnetUser {
	pub id: i32,
	pub username: String,
}


#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = telegram)]
#[diesel(primary_key(telegram_id))]
#[diesel(check_for_backend(Pg))]
pub struct TelegramUser {
	pub user_id: i32,
	pub telegram_id: i64,
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = discord)]
#[diesel(primary_key(discord_id))]
#[diesel(check_for_backend(Pg))]
pub struct DiscordUser {
	pub user_id: i32,
	pub discord_id: i64,
}


#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = steam)]
#[diesel(primary_key(steam_id))]
#[diesel(check_for_backend(Pg))]
pub struct SteamUser {
	pub user_id: i32,
	pub steam_id: i64,
}


#[cfg(feature = "service_brooch")]
#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = brooch_match)]
#[diesel(check_for_backend(Pg))]
pub struct BroochMatch {
	pub id: i64,
}

#[derive(Debug, Clone, PartialEq, Insertable)]
#[diesel(table_name = diario)]
#[diesel(check_for_backend(Pg))]
pub struct DiarioAddition {
	pub saver_id: Option<i32>,
	pub warning: Option<String>,
	pub quote: String,
	pub quoted_name: Option<String>,
	pub context: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = diario)]
#[diesel(check_for_backend(Pg))]
pub struct Diario {
	pub id: i32,
	pub saver_id: Option<i32>,
	pub saved_on: Option<chrono::NaiveDateTime>,
	pub quoted_id: Option<i32>,
	pub quoted_name: Option<String>,
	pub warning: Option<String>,
	pub quote: String,
	pub context: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Insertable)]
#[diesel(table_name = matchmaking_events)]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingEventAddition {
	pub text: String,
	pub starts_at: chrono::NaiveDateTime,
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = matchmaking_events)]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingEvent {
	pub id: i32,
	pub text: String,
	pub starts_at: chrono::NaiveDateTime,
}

#[derive(Debug, Clone, Copy, PartialEq, FromSqlRow, AsExpression)]
#[diesel(sql_type = sql_types::MatchmakingChoice)]
pub enum MatchmakingChoice {
	Yes,
	Late,
	Maybe,
	DontWait,
	Cant,
	Wont,
}

impl ToSql<sql_types::MatchmakingChoice, Pg> for MatchmakingChoice {
	fn to_sql(&self, out: &mut diesel::serialize::Output<Pg>) -> diesel::serialize::Result {
		match *self {
			Self::Yes => out.write_all(b"yes")?,
			Self::Late => out.write_all(b"late")?,
			Self::Maybe => out.write_all(b"maybe")?,
			Self::DontWait => out.write_all(b"dontw")?,
			Self::Cant => out.write_all(b"cant")?,
			Self::Wont => out.write_all(b"wont")?,
		};
		Ok(IsNull::No)
	}
}

impl FromSql<sql_types::MatchmakingChoice, Pg> for MatchmakingChoice {
	fn from_sql(raw: PgValue) -> diesel::deserialize::Result<Self> {
		match raw.as_bytes() {
			b"yes" => Ok(Self::Yes),
			b"late" => Ok(Self::Late),
			b"maybe" => Ok(Self::Maybe),
			b"dontw" => Ok(Self::DontWait),
			b"cant" => Ok(Self::Cant),
			b"wont" => Ok(Self::Wont),
			_ => Err("Unknown MatchmakingReply".into())
		}
	}
}

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
