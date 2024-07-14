use graphql_client::GraphQLQuery;

pub(self) mod config;

const STRATZ_GRAPHQL_API_URL: &str = "https://api.stratz.com/graphql";

// Bind these weird types used in the STRATZ API
type Short = i16;
type Long = i64;
type Byte = u8;

#[derive(Debug, Clone, Copy)]
pub struct GuildId(pub i64);

impl From<i64> for GuildId {
	fn from(value: i64) -> Self {
		Self(value)
	}
}

#[derive(GraphQLQuery)]
#[graphql(schema_path="src/stratz/schema.json", query_path="src/stratz/query_guild_matches.gql", response_derives="Debug, Clone")]
struct GuildMatchesQuery;


#[derive(Debug, Clone)]
enum QueryError {
	Requesting,
	Parsing,
}

type GuildMatchesQueryResponse = graphql_client::Response<guild_matches_query::ResponseData>;

pub use guild_matches_query::LobbyTypeEnum as LobbyType;
pub use guild_matches_query::GameModeEnumType as GameMode;
pub use guild_matches_query::GuildMatchesQueryGuild as Guild;
pub use guild_matches_query::GuildMatchesQueryGuildMatches as Match;
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayers as Player;
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayersHero as Hero;
pub use guild_matches_query::GuildMatchesQueryGuildMatchesPlayersSteamAccount as Steam;

/// Get the latest 10 matches of a certain Dota 2 guild.
pub async fn query_guild_matches(client: reqwest::Client, guild_id: &GuildId) -> Result<GuildMatchesQueryResponse, QueryError> {
	log::trace!("Configuring query variables...");
	let params = guild_matches_query::Variables {
		guild_id: guild_id.0,
	};

	log::trace!("Building query...");
	let body = GuildMatchesQuery::build_query(params);

	log::trace!("Building API URL...");
	let url = format!("{}?token={}", STRATZ_GRAPHQL_API_URL, config::STRATZ_TOKEN());

	log::trace!("Making request...");
	let response = client.post(url)
		.json(&body)
		.send().await
		.map_err(|_| QueryError::Requesting)?
		.json::<GuildMatchesQueryResponse>().await
		.map_err(|_| QueryError::Parsing)?;

	log::trace!("Request successful, returning...");
	Ok(response)
}