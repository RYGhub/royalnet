use diesel::{Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;
use super::schema::{users, telegram, discord, steam};


#[derive(Debug, Clone, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = users)]
#[diesel(check_for_backend(Pg))]
pub struct RoyalnetUser {
	pub id: i32,
	pub username: String,
}


#[derive(Debug, Clone, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = telegram)]
#[diesel(primary_key(telegram_id))]
#[diesel(check_for_backend(Pg))]
pub struct TelegramUser {
	pub user_id: i32,
	pub telegram_id: i64,
}


#[derive(Debug, Clone, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = discord)]
#[diesel(primary_key(discord_id))]
#[diesel(check_for_backend(Pg))]
pub struct DiscordUser {
	pub user_id: i32,
	pub discord_id: i64,
}


#[derive(Debug, Clone, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = steam)]
#[diesel(primary_key(steam_id))]
#[diesel(check_for_backend(Pg))]
pub struct SteamUser {
	pub user_id: i32,
	pub steam_id: i64,
}
