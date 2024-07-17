#![allow(unused_imports)]

use graphql_client::GraphQLQuery;
use reqwest::Url;
pub use super::Short;
pub use super::Long;
pub use super::Byte;
pub use super::QueryError as Error;

#[derive(graphql_client::GraphQLQuery)]
#[graphql(
	schema_path = "src/interfaces/stratz/schema.json",
	query_path = "src/interfaces/stratz/query_guild_matches.gql",
	response_derives = "Debug, Clone"
)]
struct Query;

pub type QueryResponse = graphql_client::Response<query::ResponseData>;
pub type QueryResult = Result<QueryResponse, Error>;

pub use query::LobbyTypeEnum as LobbyType;
pub use query::GameModeEnumType as GameMode;
pub use query::MatchLaneType as Lane;
pub use query::MatchPlayerRoleType as Role;
pub use query::QueryGuild as Guild;
pub use query::QueryGuildMatches as Match;
pub use query::QueryGuildMatchesPlayers as Player;
pub use query::QueryGuildMatchesPlayersHero as Hero;
pub use query::QueryGuildMatchesPlayersSteamAccount as Steam;
pub use query::QueryGuildMatchesPlayersStatsMatchPlayerBuffEvent as Buff;

pub async fn query(client: &reqwest::Client, url: Url, guild_id: i64) -> QueryResult {
	log::debug!("Querying guild_matches of guild {guild_id}...");
	log::trace!("Using client: {client:?}");
	log::trace!("Using API at: {url:?}");

	log::trace!("Configuring query variables...");
	let vars = query::Variables { guild_id };

	log::trace!("Building query...");
	let body = Query::build_query(vars);

	log::trace!("Making request...");
	let response = client.post(url)
		.json(&body)
		.send()
		.await
		.map_err(|_| Error::Requesting)?
		.json::<QueryResponse>()
		.await
		.map_err(|_| Error::Parsing)?;

	Ok(response)
}
