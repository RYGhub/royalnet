use anyhow::Context;
use diesel::{AsExpression, FromSqlRow, Identifiable, Insertable, PgConnection, Queryable, QueryDsl, RunQueryDsl, Selectable};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::ToSql;

use crate::newtype_sql;
use crate::utils::anyhow_result::AnyResult;

use super::super::schema::brooch_match;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable)]
#[diesel(table_name = brooch_match)]
#[diesel(check_for_backend(Pg))]
pub struct BroochMatch {
	pub id: DotaMatchId,
}

impl BroochMatch {
	pub fn is_flagged(database: &mut PgConnection, match_id: DotaMatchId) -> AnyResult<bool> {
		use crate::interfaces::database::query_prelude::*;
		use schema::brooch_match;
		
		log::trace!("Checking if {match_id:?} is flagged...");
		
		Ok(
			brooch_match::table
				.find(match_id)
				.count()
				.execute(database)
				.context("Impossibile determinare se la partita è marcata come processata nel database RYG.")?
				.gt(&0usize)
		)
	}
	
	pub fn flag(database: &mut PgConnection, match_id: DotaMatchId) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;
		use schema::brooch_match;
		
		log::debug!("Flagging {match_id:?} as parsed...");
		
		diesel::insert_into(brooch_match::table)
			.values(brooch_match::id.eq(match_id))
			.on_conflict_do_nothing()
			.get_result::<Self>(database)
			.context("Impossibile marcare la partita come processata nel database RYG.")
	}
}

newtype_sql!(pub DotaMatchId: diesel::sql_types::Int8 as i64);
