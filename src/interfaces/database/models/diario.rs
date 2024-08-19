use diesel::{Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use crate::interfaces::database::models::users::RoyalnetUserId;
use crate::newtype_sql;

use super::super::schema::diario;

#[derive(Debug, Clone, PartialEq, Insertable)]
#[diesel(table_name = diario)]
#[diesel(check_for_backend(Pg))]
pub struct DiarioAddition {
	pub saver_id: Option<RoyalnetUserId>,
	pub warning: Option<String>,
	pub quote: String,
	pub quoted_name: Option<String>,
	pub context: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = diario)]
#[diesel(check_for_backend(Pg))]
pub struct Diario {
	pub id: DiarioId,
	pub saver_id: Option<RoyalnetUserId>,
	pub saved_on: Option<chrono::NaiveDateTime>,
	pub quoted_id: Option<RoyalnetUserId>,
	pub quoted_name: Option<String>,
	pub warning: Option<String>,
	pub quote: String,
	pub context: Option<String>,
}

newtype_sql!(pub DiarioId: diesel::sql_types::Int4 as i32);
