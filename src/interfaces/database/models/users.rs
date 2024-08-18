use diesel::{Identifiable, Insertable, Queryable, Selectable};
use diesel::deserialize::FromSql;
use diesel::pg::Pg;
use diesel::serialize::ToSql;
use crate::newtype_sql;
use super::super::schema::users;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = users)]
#[diesel(check_for_backend(Pg))]
pub struct RoyalnetUser {
	pub id: RoyalnetUserId,
	pub username: String,
}

newtype_sql!(pub RoyalnetUserId: diesel::sql_types::Int4 as i32);
