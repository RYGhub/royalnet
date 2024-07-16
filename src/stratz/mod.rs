use graphql_client::GraphQLQuery;
use reqwest::Client;
use thiserror::Error;

pub(self) mod config;

const STRATZ_GRAPHQL_API_URL: &str = "https://api.stratz.com/graphql";

// Bind these weird types used in the STRATZ API
type Short = i16;
type Long = i64;
type Byte = u8;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct GuildId(pub i64);

impl From<i64> for GuildId {
	fn from(value: i64) -> Self {
		Self(value)
	}
}

#[derive(GraphQLQuery)]
#[graphql(schema_path="src/stratz/schema.json", query_path="src/stratz/query_guild_matches.gql", response_derives="Debug, Clone")]
pub struct GuildMatchesQuery;


#[derive(Debug, Clone, Error)]
pub enum QueryError {
	#[error("GraphQL request failed")]
	Requesting,
	#[error("GraphQL response parsing failed")]
	Parsing,
}

type GuildMatchesQueryResponse = graphql_client::Response<guild_matches_query::ResponseData>;

#[allow(unused_imports)]
pub use guild_matches_query::LobbyTypeEnum as LobbyType;
#[allow(unused_imports)]
pub use guild_matches_query::GameModeEnumType as GameMode;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuild as Guild;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuildMatches as Match;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayers as Player;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayersHero as Hero;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayersSteamAccount as Steam;
#[allow(unused_imports)]
pub use guild_matches_query::MatchPlayerRoleType as Role;
#[allow(unused_imports)]
pub use guild_matches_query::MatchLaneType as Lane;
#[allow(unused_imports)]
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayersStatsMatchPlayerBuffEvent as Buff;


/// Get the latest 10 matches of a certain Dota 2 guild.
pub async fn query_guild_matches(client: &Client, guild_id: &GuildId) -> Result<GuildMatchesQueryResponse, QueryError> {
	log::debug!("Querying guild matches with {client:?} for {guild_id:?}...");

	log::trace!("Configuring query variables...");
	let params = guild_matches_query::Variables {
		guild_id: guild_id.0,
	};

	log::trace!("Building query...");
	let body = GuildMatchesQuery::build_query(params);

	log::trace!("Building API URL...");
	let url = format!("{}?jwt={}", STRATZ_GRAPHQL_API_URL, config::STRATZ_TOKEN());
	log::trace!("STRATZ API URL is: {url:?}");

	log::trace!("Making request...");
	let response = client.post(url)
		.json(&body)
		.send().await
		.map_err(|_| QueryError::Requesting)?
		.json::<GuildMatchesQueryResponse>().await
		.map_err(|_| QueryError::Parsing)?;

	log::trace!("Request successful!");
	Ok(response)
}