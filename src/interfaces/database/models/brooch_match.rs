use diesel::{Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use super::super::schema::brooch_match;

#[cfg(feature = "service_brooch")]
#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = brooch_match)]
#[diesel(check_for_backend(Pg))]
pub struct BroochMatch {
	pub id: i64,
}
