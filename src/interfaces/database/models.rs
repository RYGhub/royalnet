use diesel::{Identifiable, Insertable, Queryable, Selectable, Associations};
use diesel::pg::Pg;
use super::schema::{users, telegram, discord, steam, brooch_match, diario};


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

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = diario)]
#[diesel(check_for_backend(Pg))]
pub struct DiarioEntry {
	pub id: i32,
	pub warning: Option<String>,
	pub quote: String,
	pub quoted_name: Option<String>,
	pub context: Option<String>,
}