use diesel::{Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use super::super::schema::users;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = users)]
#[diesel(check_for_backend(Pg))]
pub struct RoyalnetUser {
	pub id: i32,
	pub username: String,
}
