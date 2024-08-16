use std::io::Write;
use diesel::{Identifiable, Insertable, Queryable, Selectable, Associations, FromSqlRow, AsExpression};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::{IsNull, ToSql};
use crate::interfaces::database::schema::sql_types::MatchmakingReplyType;
use super::schema::{users, telegram, discord, steam, brooch_match, diario, matchmaking, matchmade};


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
pub struct DiarioEntry {
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
#[diesel(table_name = matchmaking)]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingAddition {
	pub text: String,
	pub starts_at: chrono::NaiveDateTime,
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = matchmaking)]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingEntry {
	pub id: i32,
	pub text: String,
	pub starts_at: chrono::NaiveDateTime,
}

#[derive(Debug, Clone, PartialEq, FromSqlRow, AsExpression)]
#[diesel(sql_type = MatchmakingReplyType)]
pub enum MatchmakingReply {
	Yes,
	Late,
	Maybe,
	DontWait,
	Cant,
	Wont,
}

impl ToSql<MatchmakingReplyType, Pg> for MatchmakingReply {
	fn to_sql(&self, out: &mut diesel::serialize::Output<Pg>) -> diesel::serialize::Result {
		match *self {
			MatchmakingReply::Yes => out.write_all(b"yes")?,
			MatchmakingReply::Late => out.write_all(b"late")?,
			MatchmakingReply::Maybe => out.write_all(b"maybe")?,
			MatchmakingReply::DontWait => out.write_all(b"dontw")?,
			MatchmakingReply::Cant => out.write_all(b"cant")?,
			MatchmakingReply::Wont => out.write_all(b"wont")?,
		};
		Ok(IsNull::No)
	}
}

impl FromSql<MatchmakingReplyType, Pg> for MatchmakingReply {
	fn from_sql(raw: PgValue) -> diesel::deserialize::Result<Self> {
		match raw.as_bytes() {
			b"yes" => Ok(MatchmakingReply::Yes),
			b"late" => Ok(MatchmakingReply::Late),
			b"maybe" => Ok(MatchmakingReply::Maybe),
			b"dontw" => Ok(MatchmakingReply::DontWait),
			b"cant" => Ok(MatchmakingReply::Cant),
			b"wont" => Ok(MatchmakingReply::Wont),
			_ => Err("Unknown MatchmakingReply".into())
		}
	}
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(MatchmakingEntry, foreign_key = matchmaking_id))]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = matchmade)]
#[diesel(primary_key(matchmaking_id, user_id))]
#[diesel(check_for_backend(Pg))]
pub struct Matchmade {
	pub matchmaking_id: i32,
	pub user_id: i32,
	pub reply: MatchmakingReply,
	pub late_mins: i32,
}
