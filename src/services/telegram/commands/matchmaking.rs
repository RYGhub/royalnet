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
use crate::interfaces::database::models::{Matchmade, MatchmakingAddition, MatchmakingEntry, MatchmakingReply, MatchMessageTelegram, RoyalnetUser, TelegramUser};
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
	replies: Vec<(Matchmade, RoyalnetUser, TelegramUser)>,
}

impl TelegramWrite for (Matchmade, RoyalnetUser, TelegramUser) {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
	where
		T: Write
	{
		let emoji = match self.0.reply {
			MatchmakingReply::Yes => "🔵",
			MatchmakingReply::Late => match self.0.late_mins {
				i32::MIN..=5 => "🕐",
				6..=10 => "🕑",
				11..=15 => "🕒",
				16..=20 => "🕓",
				21..=25 => "🕔",
				26..=30 => "🕕",
				31..=35 => "🕖",
				36..=40 => "🕗",
				41..=45 => "🕘",
				46..=50 => "🕙",
				51..=55 => "🕚",
				56..=i32::MAX => "🕛",
			},
			MatchmakingReply::Maybe => "❔",
			MatchmakingReply::DontWait => "❓",
			MatchmakingReply::Cant => "🔺",
			MatchmakingReply::Wont => "🔻",
		};

		let telegram_id = self.2.telegram_id;
		let username = &self.1.username;

		write!(f, "{emoji} <a href=\"tg://user?id={telegram_id}\">{username}</a>")?;

		if self.0.reply == MatchmakingReply::Late {
			let late_mins = &self.0.late_mins;

			write!(f, " (+{late_mins} mins)")?;
		}

		Ok(())
	}
}

impl TelegramWrite for MatchmakingData {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
	where
		T: Write
	{
		let now = chrono::Local::now().naive_local();

		let emoji = match self.entry.starts_at.cmp(&now) {
			Ordering::Greater => "🚩",
			_ => "🔔",
		};

		let text = self.entry.text.clone().escape_telegram_html();
		writeln!(f, "{} <b>{}</b>", &emoji, &text)?;

		let start = self.entry.starts_at.format("%c").to_string().escape_telegram_html();
		writeln!(f, "<i>{}</i>", &start)?;

		writeln!(f)?;

		for reply in self.replies.iter() {
			reply.write_telegram(f)?;
			writeln!(f)?;
		}

		Ok(())
	}
}

const DATA_YES: &str = "yes";
const DATA_5MIN: &str = "5min";
const DATA_15MIN: &str = "15min";
const DATA_60MIN: &str = "60min";
const DATA_MAYBE: &str = "maybe";
const DATA_DONTW: &str = "dontw";
const DATA_CANT: &str = "cant";
const DATA_WONT: &str = "wont";

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

	let replies = vec![];

	let data = MatchmakingData { entry, replies };

	let prefix = format!("matchmaking:{}", data.entry.id);

	let button = move |text: &str, data: &str| -> InlineKeyboardButton {
		InlineKeyboardButton::new(
			text,
			InlineKeyboardButtonKind::CallbackData(
				format!("{}:{}", prefix, data)
			)
		)
	};

	let button_yes = button("🔵 Ci sarò!", DATA_YES);
	let button_5min = button("🕐 +5 min", DATA_5MIN);
	let button_15min = button("🕒 +15 min", DATA_15MIN);
	let button_60min = button("🕛 +60 min", DATA_60MIN);
	let button_maybe = button("❔ Forse...", DATA_MAYBE);
	let button_dontw = button("❓ Non aspettatemi.", DATA_DONTW);
	let button_cant = button("🔺 Non posso...", DATA_CANT);
	let button_wont = button("🔻 Non mi interessa.", DATA_WONT);

	let im = InlineKeyboardMarkup::new(vec![
		vec![button_yes],
		vec![button_5min, button_15min, button_60min],
		vec![button_maybe, button_dontw],
		vec![button_cant, button_wont],
	]);

	let reply = bot
		.send_message(message.chat.id, data.to_string_telegram())
		.parse_mode(ParseMode::Html)
		.reply_to_message_id(message.id)
		.reply_markup(im)
		.await
		.context("Non è stato possibile inviare il matchmaking.")?;

	let mmm = MatchMessageTelegram {
		matchmaking_id: data.entry.id,
		telegram_message_id: reply.id.0,
	};

	let mmm = {
		use diesel::prelude::*;
		use diesel::dsl::*;
		use crate::interfaces::database::schema::matchmessage_telegram::dsl::*;

		insert_into(matchmessage_telegram)
			.values(&addition)
			.get_result::<MatchMessageTelegram>(&mut database)
			.context("Non è stato possibile aggiungere il messaggio Telegram al database RYG.")?
	};

	let wait_duration = determine_wait(args.start);

	tokio::time::sleep(wait_duration).await;

	bot
		.delete_message(reply.chat.id, reply.id)
		.await
		.context("Non è stato possibile eliminare il matchmaking.")?;

	let entry = {
		use diesel::prelude::*;
		use crate::interfaces::database::schema::matchmaking::dsl::*;

		matchmaking
			.filter(id.eq(data.entry.id))
			.get_result::<MatchmakingEntry>(&mut database)
			.context("Non è stato possibile trovare il matchmaking nel database RYG.")?
	};

	let replies = {
		use diesel::prelude::*;
		use crate::interfaces::database::schema::{matchmade, users, telegram};

		matchmade::table
			.filter(matchmade::matchmaking_id.eq(entry.id))
			.inner_join(users::table.on(matchmade::user_id.eq(users::id)))
			.inner_join(telegram::table.on(users::id.eq(telegram::user_id)))
			.get_results::<(Matchmade, RoyalnetUser, TelegramUser)>(&mut database)
			.context("Non è stato possibile trovare le risposte al matchmaking nel database RYG.")?
	};

	let data = MatchmakingData { entry, replies };

	let _reply = bot
		.send_message(message.chat.id, data.to_string_telegram())
		.parse_mode(ParseMode::Html)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la notifica di inizio evento.")?;

	Ok(())
}