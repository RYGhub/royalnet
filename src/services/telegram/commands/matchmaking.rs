use std::str::FromStr;
use anyhow::Context;
use once_cell::sync::Lazy;
use parse_datetime::parse_datetime_at_date;
use regex::Regex;
use teloxide::Bot;
use teloxide::prelude::Message;
use crate::services::telegram::commands::CommandResult;
use crate::services::telegram::deps::interface_database::DatabaseInterface;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MatchmakingArgs {
	target: chrono::DateTime<chrono::Local>,
	text: String,
}

impl FromStr for MatchmakingArgs {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		static REGEX: Lazy<Regex> = Lazy::new(|| Regex::new(r"\[(?<target>.*)]\s*(?<text>.+)$").unwrap());

		let captures = REGEX.captures(s)
			.context("Sintassi del comando incorretta.")?;

		let target = captures.name("target")
			.unwrap()
			.as_str();

		let text = captures.name("text")
			.unwrap()
			.as_str()
			.to_string();

		let target = parse_datetime_at_date(chrono::Local::now(), target)
			.context("Impossibile determinare la data in cui l'attesa avrà termine.")?
			.with_timezone(&chrono::Local);

		Ok(
			Self { target, text }
		)
	}
}

pub async fn handler(bot: &Bot, message: &Message, args: MatchmakingArgs, database: &DatabaseInterface) -> CommandResult {
	todo!()
}