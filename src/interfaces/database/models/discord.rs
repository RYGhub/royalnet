use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;
use crate::newtype_sql;
use super::super::schema::discord;
use super::users::{RoyalnetUser, RoyalnetUserId};

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = discord)]
#[diesel(primary_key(discord_id))]
#[diesel(check_for_backend(Pg))]
pub struct DiscordUser {
	pub user_id: RoyalnetUserId,
	pub discord_id: DiscordUserId,
}

newtype_sql!(pub DiscordUserId: diesel::sql_types::Int8 as i64);
