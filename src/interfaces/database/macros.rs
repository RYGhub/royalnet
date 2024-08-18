#[macro_export]
macro_rules! newtype_sql {
    ($visibility: vis $newtype: ident: $sqltype: path as $rusttype: path) => {
		#[repr(transparent)]
		#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, diesel::FromSqlRow, diesel::AsExpression)]
		#[diesel(sql_type = $sqltype)]
		$visibility struct $newtype(pub $rusttype);

		impl std::fmt::Display for $newtype {
			fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> Result<(), std::fmt::Error> {
				write!(f, "{}", self.0)
			}
		}

		impl From<$rusttype> for $newtype {
			fn from(value: $rusttype) -> Self {
				Self(value)
			}
		}

		impl From<$newtype> for $rusttype {
			fn from(value: $newtype) -> Self {
				value.0
			}
		}

		impl diesel::serialize::ToSql<$sqltype, diesel::pg::Pg> for $newtype {
			fn to_sql<'a>(&'a self, out: &mut diesel::serialize::Output<'a, '_, diesel::pg::Pg>) -> diesel::serialize::Result {
				use diesel::serialize::ToSql;

				ToSql::<$sqltype, diesel::pg::Pg>::to_sql(&self.0, out)
			}
		}

		impl diesel::deserialize::FromSql<$sqltype, diesel::pg::Pg> for $newtype {
			fn from_sql(raw: diesel::pg::PgValue) -> diesel::deserialize::Result<Self> {
				use diesel::deserialize::FromSql;

				FromSql::<$sqltype, diesel::pg::Pg>::from_sql(raw)
					.map(Self)
			}
		}

		impl std::str::FromStr for $newtype {
			type Err = anyhow::Error;

			fn from_str(s: &str) -> Result<Self, Self::Err> {
				use anyhow::Context;

				Ok(
					Self(
						s.parse::<$rusttype>()
							.context("Impossible convertire a newtype.")?
					)
				)
			}
		}
	};
}