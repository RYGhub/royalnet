use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;
use crate::newtype_sql;
use super::super::schema::steam;
use super::users::{RoyalnetUser, RoyalnetUserId};

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = steam)]
#[diesel(primary_key(steam_id))]
#[diesel(check_for_backend(Pg))]
pub struct SteamUser {
	pub user_id: RoyalnetUserId,
	pub steam_id: SteamId64,
}

newtype_sql!(pub SteamId64: diesel::sql_types::Int8 as i64);
