use thiserror::Error;

pub type Short = i16;
pub type Long = i64;
pub type Byte = u8;

#[derive(Debug, Clone, Error)]
pub enum QueryError {
	#[error("GraphQL request failed")]
	Requesting,
	#[error("GraphQL response parsing failed")]
	Parsing,
}

pub mod guild_matches;
