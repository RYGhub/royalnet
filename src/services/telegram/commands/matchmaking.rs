use std::str::FromStr;
use anyhow::Context;
use once_cell::sync::Lazy;
use parse_datetime::parse_datetime_at_date;
use regex::Regex;
use teloxide::Bot;
use teloxide::prelude::Message;
use crate::interfaces::database::models::{MatchmakingEvent};
use crate::services::telegram::commands::CommandResult;
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::utils::time::determine_wait;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct MatchmakingArgs {
	start: chrono::DateTime<chrono::Local>,
	text: String,
}

impl FromStr for MatchmakingArgs {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		static REGEX: Lazy<Regex> = Lazy::new(|| Regex::new(r"\[(?<start>.*)]\s*(?<text>.+)$").unwrap());

		let captures = REGEX.captures(s)
			.context("Sintassi del comando incorretta.")?;

		let start = captures.name("start")
			.unwrap()
			.as_str();

		let text = captures.name("text")
			.unwrap()
			.as_str()
			.to_string();

		let start = parse_datetime_at_date(chrono::Local::now(), start)
			.context("Impossibile determinare la data in cui l'attesa avrà termine.")?
			.with_timezone(&chrono::Local);

		Ok(
			Self { start, text }
		)
	}
}

pub async fn handler(bot: &Bot, message: &Message, args: &MatchmakingArgs, database: &DatabaseInterface) -> CommandResult {
	let mut database = database.connect()?;

	let event = MatchmakingEvent::create(&mut database, &args.text, &args.start)
		.context("Non è stato possibile creare un nuovo matchmaking.")?;

	let reply = event.poll_telegram(&mut database, bot, message.chat.id, Some(message.id))
		.await
		.context("Non è stato possibile postare il matchmaking.")?;

	tokio::time::sleep(determine_wait(&args.start)).await;

	reply.delete(&mut database, bot)
		.await
		.context("Non è stato possibile eliminare il matchmaking.")?;

	event.notify_telegram(&mut database, bot, message.chat.id, Some(message.id))
		.await
		.context("Non è stato possibile confermare il matchmaking.")?;

	Ok(())
}
