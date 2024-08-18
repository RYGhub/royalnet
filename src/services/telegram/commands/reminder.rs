use std::str::FromStr;
use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message, ParseMode, ReplyParameters};
use parse_datetime::parse_datetime_at_date;
use once_cell::sync::Lazy;
use regex::Regex;
use crate::utils::telegram_string::TelegramEscape;
use crate::utils::time::sleep_chrono;
use super::CommandResult;


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

pub async fn handler(bot: &Bot, message: &Message, ReminderArgs { target, reminder }: &ReminderArgs) -> CommandResult {
	let text = format!(
		"🕒 <b>Promemoria impostato</b>\n\
		<i>{}</i>\n\
		\n\
		{}",
		target.format("%c").to_string().escape_telegram_html(),
		reminder.clone().escape_telegram_html()
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare la conferma del promemoria.")?;

	sleep_chrono(target).await;

	let text = format!(
		"🕒 <b>Promemoria attivato</b>\n\
		<i>{}</i>\n\
		\n\
		{}",
		target.format("%c").to_string().escape_telegram_html(),
		reminder.escape_telegram_html()
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare il promemoria.")?;

	Ok(())
}
