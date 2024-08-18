use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use super::super::schema::steam;
use super::users::RoyalnetUser;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = steam)]
#[diesel(primary_key(steam_id))]
#[diesel(check_for_backend(Pg))]
pub struct SteamUser {
	pub user_id: i32,
	pub steam_id: i64,
}