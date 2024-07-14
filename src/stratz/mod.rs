use graphql_client::GraphQLQuery;

pub(self) mod config;

// Bind these weird types used in the STRATZ API
type Short = i16;
type Long = i64;
type Byte = u8;

