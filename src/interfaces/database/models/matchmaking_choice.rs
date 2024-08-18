use std::io::Write;

use diesel::{AsExpression, FromSqlRow};
use diesel::deserialize::FromSql;
use diesel::pg::{Pg, PgValue};
use diesel::serialize::{IsNull, ToSql};

use super::super::schema::sql_types;

#[derive(Debug, Clone, Copy, PartialEq, FromSqlRow, AsExpression)]
#[diesel(sql_type = sql_types::MatchmakingChoice)]
pub enum MatchmakingChoice {
	Yes,
	Late,
	Maybe,
	DontWait,
	Cant,
	Wont,
}

impl ToSql<sql_types::MatchmakingChoice, Pg> for MatchmakingChoice {
	fn to_sql(&self, out: &mut diesel::serialize::Output<Pg>) -> diesel::serialize::Result {
		match *self {
			Self::Yes => out.write_all(b"yes")?,
			Self::Late => out.write_all(b"late")?,
			Self::Maybe => out.write_all(b"maybe")?,
			Self::DontWait => out.write_all(b"dontw")?,
			Self::Cant => out.write_all(b"cant")?,
			Self::Wont => out.write_all(b"wont")?,
		};
		Ok(IsNull::No)
	}
}

impl FromSql<sql_types::MatchmakingChoice, Pg> for MatchmakingChoice {
	fn from_sql(raw: PgValue) -> diesel::deserialize::Result<Self> {
		match raw.as_bytes() {
			b"yes" => Ok(Self::Yes),
			b"late" => Ok(Self::Late),
			b"maybe" => Ok(Self::Maybe),
			b"dontw" => Ok(Self::DontWait),
			b"cant" => Ok(Self::Cant),
			b"wont" => Ok(Self::Wont),
			_ => Err("Unknown MatchmakingReply".into())
		}
	}
}