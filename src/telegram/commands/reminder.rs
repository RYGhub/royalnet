use std::str::FromStr;
use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use parse_datetime::parse_datetime_at_date;
use once_cell::sync::Lazy;
use regex::Regex;
use super::{CommandResult};


fn determine_wait(target_chrono: chrono::DateTime<chrono::Local>) -> tokio::time::Duration {
	let now_chrono = chrono::Local::now();

	let duration_chrono = target_chrono.signed_duration_since(now_chrono);
	let seconds = duration_chrono.num_seconds();

	tokio::time::Duration::from_secs(seconds as u64)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReminderArgs {
	target: chrono::DateTime<chrono::Local>,
	reminder: String,
}

impl FromStr for ReminderArgs {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		static REGEX: Lazy<Regex> = Lazy::new(|| Regex::new(r"\[(?<target>.*)]\s*(?<reminder>.+)$").unwrap());

		let captures = REGEX.captures(s)
			.context("Sintassi del comando incorretta.")?;

		let target = captures.name("target")
			.unwrap()
			.as_str();

		let reminder = captures.name("reminder")
			.unwrap()
			.as_str()
			.to_string();

		let target = parse_datetime_at_date(chrono::Local::now(), target)
			.context("Impossibile determinare la data in cui l'attesa avrà termine.")?
			.with_timezone(&chrono::Local);

		Ok(
			ReminderArgs { target, reminder }
		)
	}
}

pub async fn handler(bot: &Bot, message: &Message, ReminderArgs { target, reminder}: ReminderArgs) -> CommandResult {
	let text = format!(
		"🕒 Promemoria per {} impostato\n\
		{}",
		target.format("%c"),
		reminder
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la conferma.")?;

	let wait_duration = determine_wait(target);

	tokio::time::sleep(wait_duration).await;

	let text = format!(
		"🕒 Promemoria per {} attivato\n\
		{}",
		target.format("%c"),
		reminder
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare il promemoria.")?;

	Ok(())
}
