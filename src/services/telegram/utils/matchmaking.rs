use std::cmp::Ordering;
use std::fmt::{Error, Write};
use std::str::FromStr;
use anyhow::Context;
use diesel::PgConnection;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{ChatId, InlineKeyboardButton, InlineKeyboardButtonKind, InlineKeyboardMarkup, Message, MessageId, ParseMode};
use crate::interfaces::database::models::{MatchmakingChoice, MatchmakingEvent, MatchmakingMessageTelegram, MatchmakingReply, RoyalnetUser, TelegramUser};
use crate::utils::escape::TelegramEscape;
use crate::utils::write::TelegramWrite;

impl MatchmakingEvent {
	pub async fn poll_telegram(&self, database: &mut PgConnection, bot: &Bot, chat_id: ChatId, reply_to: Option<MessageId>) -> anyhow::Result<MatchmakingMessageTelegram> {
		MatchmakingMessageTelegram::create(database, self.id, bot, chat_id, reply_to).await
	}

	pub async fn notify_telegram(&self, database: &mut PgConnection, bot: &Bot, chat_id: ChatId, reply_to: Option<MessageId>) -> anyhow::Result<Message> {
		let replies = MatchmakingReply::get_all_telegram(database, self.id)?;
		let data = (self, &replies);

		let mut reply = bot.send_message(chat_id, data.to_string_telegram());
		reply = reply.parse_mode(ParseMode::Html);

		if let Some(reply_to) = reply_to {
			reply = reply.reply_to_message_id(reply_to);
		}

		let reply = reply.await?;

		Ok(reply)
	}
}

impl TelegramWrite for (&MatchmakingEvent, &Vec<(MatchmakingReply, RoyalnetUser, TelegramUser)>) {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
	where
		T: Write
	{
		let now = chrono::Local::now().naive_local();

		let emoji = match self.0.starts_at.cmp(&now) {
			Ordering::Greater => "🚩",
			_ => "🔔",
		};

		let text = self.0.text.clone().escape_telegram_html();
		writeln!(f, "{emoji} <b>{text}</b>")?;

		let start = self.0.starts_at.format("%c").to_string().escape_telegram_html();
		writeln!(f, "<i>{start}</i>")?;

		writeln!(f)?;

		for reply_tuple in self.1.iter() {
			writeln!(f, "{}", reply_tuple.to_string_telegram())?;
		}

		Ok(())
	}
}

impl MatchmakingReply {
	pub fn get_all_telegram(database: &mut PgConnection, matchmaking_id: i32) -> anyhow::Result<Vec<(MatchmakingReply, RoyalnetUser, TelegramUser)>> {
		use diesel::prelude::*;
		use crate::interfaces::database::schema::{matchmaking_replies, users, telegram};

		matchmaking_replies::table
			.filter(matchmaking_replies::matchmaking_id.eq(matchmaking_id))
			.inner_join(users::table.on(matchmaking_replies::user_id.eq(users::id)))
			.inner_join(telegram::table.on(users::id.eq(telegram::user_id)))
			.get_results::<(MatchmakingReply, RoyalnetUser, TelegramUser)>(database)
			.context("Non è stato possibile recuperare le risposte al matchmaking dal database RYG.")
	}
}

impl TelegramWrite for (MatchmakingReply, RoyalnetUser, TelegramUser) {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
	where
		T: Write
	{
		let emoji = match self.0.choice {
			MatchmakingChoice::Yes => "🔵",
			MatchmakingChoice::Late => match self.0.late_mins {
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
			MatchmakingChoice::Maybe => "❔",
			MatchmakingChoice::DontWait => "❓",
			MatchmakingChoice::Cant => "🔺",
			MatchmakingChoice::Wont => "🔻",
		};

		let telegram_id = self.2.telegram_id;
		let username = &self.1.username;

		write!(f, "{emoji} <a href=\"tg://user?id={telegram_id}\">{username}</a>")?;

		if self.0.choice == MatchmakingChoice::Late {
			let late_mins = self.0.late_mins;

			write!(f, " (+{late_mins} mins)")?;
		}

		Ok(())
	}
}

impl MatchmakingMessageTelegram {
	pub fn get_all(database: &mut PgConnection, matchmaking_id: i32) -> anyhow::Result<Vec<Self>> {
		use diesel::prelude::*;
		use crate::interfaces::database::schema::matchmaking_messages_telegram;

		matchmaking_messages_telegram::table
			.filter(matchmaking_messages_telegram::matchmaking_id.eq(matchmaking_id))
			.get_results::<MatchmakingMessageTelegram>(database)
			.context("Non è stato possibile recuperare i messaggi Telegram rappresentanti il matchmaking dal database RYG.")
	}

	fn make_callback_data_telegram_raw(matchmaking_id: i32, data: &str) -> String {
		format!("matchmaking:{}:{}", matchmaking_id, data)
	}

	fn make_callback_data_telegram_choice(matchmaking_id: i32, callback: MatchmakingTelegramKeyboardCallback) -> String {
		Self::make_callback_data_telegram_raw(matchmaking_id, callback.into())
	}

	fn make_inline_button_telegram(text: &str, matchmaking_id: i32, callback: MatchmakingTelegramKeyboardCallback) -> InlineKeyboardButton {
		InlineKeyboardButton::new(
			text,
			InlineKeyboardButtonKind::CallbackData(
				Self::make_callback_data_telegram_choice(matchmaking_id, callback)
			)
		)
	}

	fn make_reply_markup_telegram(matchmaking_id: i32) -> InlineKeyboardMarkup {
		use MatchmakingTelegramKeyboardCallback::*;

		let button_yes = Self::make_inline_button_telegram("🔵 Ci sarò!", matchmaking_id, Yes);
		let button_5min = Self::make_inline_button_telegram("🕐 +5 min", matchmaking_id, Plus5Min);
		let button_15min = Self::make_inline_button_telegram("🕒 +15 min", matchmaking_id, Plus15Min);
		let button_60min = Self::make_inline_button_telegram("🕛 +60 min", matchmaking_id, Plus60Min);
		let button_maybe = Self::make_inline_button_telegram("❔ Forse...", matchmaking_id, Maybe);
		let button_dontw = Self::make_inline_button_telegram("❓ Non aspettatemi.", matchmaking_id, DontWait);
		let button_cant = Self::make_inline_button_telegram("🔺 Non posso...", matchmaking_id, Cant);
		let button_wont = Self::make_inline_button_telegram("🔻 Non mi interessa.", matchmaking_id, Wont);

		InlineKeyboardMarkup::new(vec![
			vec![button_yes],
			vec![button_5min, button_15min, button_60min],
			vec![button_maybe, button_dontw],
			vec![button_cant, button_wont],
		])
	}

	pub async fn create(database: &mut PgConnection, matchmaking_id: i32, bot: &Bot, chat_id: ChatId, reply_to: Option<MessageId>) -> anyhow::Result<Self> {
		let event = MatchmakingEvent::get(database, matchmaking_id)?;
		let replies = MatchmakingReply::get_all_telegram(database, matchmaking_id)?;
		let data = (&event, &replies);

		let mut reply = bot.send_message(chat_id, data.to_string_telegram());
		reply = reply.parse_mode(ParseMode::Html);
		reply = reply.reply_markup(Self::make_reply_markup_telegram(matchmaking_id));

		if let Some(reply_to) = reply_to {
			reply = reply.reply_to_message_id(reply_to);
		}

		let reply = reply.await?;

		let mmt = {
			use diesel::prelude::*;
			use diesel::dsl::*;
			use crate::interfaces::database::schema::matchmaking_messages_telegram;

			insert_into(matchmaking_messages_telegram::table)
				.values(&MatchmakingMessageTelegram {
					matchmaking_id,
					telegram_chat_id: reply.chat.id.0,
					telegram_message_id: reply.id.0,
				})
				.get_result::<MatchmakingMessageTelegram>(database)
				.context("Non è stato possibile aggiungere il messaggio Telegram al database RYG.")?
		};

		Ok(mmt)
	}

	pub async fn delete(self, database: &mut PgConnection, bot: &Bot) -> anyhow::Result<()> {
		{
			use diesel::prelude::*;
			use diesel::dsl::*;
			use crate::interfaces::database::schema::matchmaking_messages_telegram;

			delete(matchmaking_messages_telegram::table)
				.filter(matchmaking_messages_telegram::matchmaking_id.eq(self.matchmaking_id))
				.filter(matchmaking_messages_telegram::telegram_chat_id.eq(self.telegram_chat_id))
				.filter(matchmaking_messages_telegram::telegram_message_id.eq(self.telegram_message_id))
				.get_result::<MatchmakingMessageTelegram>(database)
				.context("Non è stato possibile rimuovere il messaggio Telegram dal database RYG.")?;
		}

		bot
			.delete_message(ChatId(self.telegram_chat_id), MessageId(self.telegram_message_id))
			.await
			.context("Non è stato possibile eliminare il matchmaking.")?;

		Ok(())
	}
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchmakingTelegramKeyboardCallback {
	Yes,
	Plus5Min,
	Plus15Min,
	Plus60Min,
	Maybe,
	DontWait,
	Cant,
	Wont,
}

impl FromStr for MatchmakingTelegramKeyboardCallback {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		Ok(
			match s {
				"yes" => Self::Yes,
				"5min" => Self::Plus5Min,
				"15min" => Self::Plus15Min,
				"60min" => Self::Plus60Min,
				"maybe" => Self::Maybe,
				"dontw" => Self::DontWait,
				"cant" => Self::Cant,
				"wont" => Self::Wont,
				x => anyhow::bail!("Unknown keyboard callback: {x:?}"),
			}
		)
	}
}

impl From<MatchmakingTelegramKeyboardCallback> for &'static str {
	fn from(value: MatchmakingTelegramKeyboardCallback) -> Self {
		match value {
			MatchmakingTelegramKeyboardCallback::Yes => "yes",
			MatchmakingTelegramKeyboardCallback::Plus5Min => "5min",
			MatchmakingTelegramKeyboardCallback::Plus15Min => "15min",
			MatchmakingTelegramKeyboardCallback::Plus60Min => "60min",
			MatchmakingTelegramKeyboardCallback::Maybe => "maybe",
			MatchmakingTelegramKeyboardCallback::DontWait => "dontw",
			MatchmakingTelegramKeyboardCallback::Cant => "cant",
			MatchmakingTelegramKeyboardCallback::Wont => "wont",
		}
	}
}