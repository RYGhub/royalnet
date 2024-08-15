use std::cmp::Ordering;
use std::fmt::{Error, Write};
use std::str::FromStr;
use anyhow::Context;
use once_cell::sync::Lazy;
use parse_datetime::parse_datetime_at_date;
use regex::Regex;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::{Message, Requester};
use teloxide::types::{InlineKeyboardButton, InlineKeyboardButtonKind, InlineKeyboardMarkup, ParseMode};
use crate::interfaces::database::models::{MatchmakingAddition, MatchmakingEntry};
use crate::services::telegram::commands::CommandResult;
use crate::services::telegram::deps::interface_database::DatabaseInterface;
use crate::utils::telegramdisplay::{TelegramEscape, TelegramWrite};
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

#[derive(Debug, Clone, PartialEq)]
pub struct MatchmakingData {
	entry: MatchmakingEntry,
}

impl TelegramWrite for MatchmakingData {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
	where
		T: Write
	{
		let now = chrono::Local::now().naive_local();

		let emoji = match self.entry.starts_at.cmp(&now) {
			Ordering::Greater => "🔜",
			_ => "🔛",
		};

		let text = self.entry.text.clone().escape_telegram_html();
		write!(f, "{} <b>{}</b>\n", &emoji, &text)?;

		let start = self.entry.starts_at.format("%c").to_string().escape_telegram_html();
		write!(f, "<i>{}</i>\n", &start)?;

		Ok(())
	}
}

pub async fn handler(bot: &Bot, message: &Message, args: MatchmakingArgs, database: &DatabaseInterface) -> CommandResult {
	let mut database = database.connect()?;

	let addition = MatchmakingAddition {
		text: args.text,
		starts_at: args.start.naive_local(),
	};

	let entry = {
		use diesel::prelude::*;
		use diesel::dsl::*;
		use crate::interfaces::database::schema::matchmaking::dsl::*;

		insert_into(matchmaking)
			.values(&addition)
			.get_result::<MatchmakingEntry>(&mut database)
			.context("Non è stato possibile aggiungere il matchmaking al database RYG.")?
	};

	let data = MatchmakingData { entry };

	let im = InlineKeyboardMarkup::new(vec![
		vec![
			InlineKeyboardButton::new("🔵 Ci sarò!", InlineKeyboardButtonKind::CallbackData("ok".to_string())),
		],
		vec![
			InlineKeyboardButton::new("🕐 +5 min", InlineKeyboardButtonKind::CallbackData("1".to_string())),
			InlineKeyboardButton::new("🕒 +15 min", InlineKeyboardButtonKind::CallbackData("3".to_string())),
			InlineKeyboardButton::new("🕤 +60 min", InlineKeyboardButtonKind::CallbackData("9".to_string())),
		],
		vec![
			InlineKeyboardButton::new("❔ Forse...", InlineKeyboardButtonKind::CallbackData("mbw".to_string())),
			InlineKeyboardButton::new("❓ Non aspettatemi.", InlineKeyboardButtonKind::CallbackData("mb".to_string())),
		],
		vec![
			InlineKeyboardButton::new("🔺 Non posso.", InlineKeyboardButtonKind::CallbackData("cant".to_string())),
			InlineKeyboardButton::new("🔻 Non voglio.", InlineKeyboardButtonKind::CallbackData("no".to_string())),
		],
	]);

	let _reply = bot
		.send_message(message.chat.id, data.to_string_telegram())
		.parse_mode(ParseMode::Html)
		.reply_to_message_id(message.id)
		.reply_markup(im)
		.await
		.context("Non è stato possibile inviare il matchmaking.")?;

	let wait_duration = determine_wait(args.start);

	tokio::time::sleep(wait_duration).await;

	Ok(())
}