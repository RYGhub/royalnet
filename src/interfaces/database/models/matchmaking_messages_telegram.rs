use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;
use crate::interfaces::database::models::MatchmakingId;
use crate::interfaces::database::models::telegram::{TelegramChatId, TelegramMessageId};
use super::matchmaking_events::MatchmakingEvent;
use super::super::schema::matchmaking_messages_telegram;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(MatchmakingEvent, foreign_key = matchmaking_id))]
#[diesel(table_name = matchmaking_messages_telegram)]
#[diesel(primary_key(matchmaking_id, telegram_chat_id, telegram_message_id))]
#[diesel(check_for_backend(Pg))]
pub struct MatchmakingMessageTelegram {
	pub matchmaking_id: MatchmakingId,
	pub telegram_chat_id: TelegramChatId,
	pub telegram_message_id: TelegramMessageId,
}

#[cfg(feature = "service_telegram")]
pub(crate) mod telegram_ext {
	use std::cmp::Ordering;
	use std::str::FromStr;
	use anyhow::Context;
	use super::*;
	use diesel::PgConnection;
	use teloxide::payloads::SendMessageSetters;
	use teloxide::payloads::EditMessageTextSetters;
	use teloxide::requests::Requester;
	use teloxide::types::ParseMode;
	use crate::interfaces::database::models::{MatchmakingChoice, MatchmakingId, MatchmakingReply, RoyalnetUser, TelegramUser};
	use crate::utils::anyhow_result::AnyResult;
	use crate::utils::telegram_string::TelegramEscape;

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

	impl MatchmakingTelegramKeyboardCallback {
		/// Create callback data representing the [MatchmakingTelegramKeyboardCallback] in the given [MatchmakingId].
		pub fn callback_data(self, matchmaking_id: MatchmakingId) -> String {
			matchmaking_id.callback_data(self.into())
		}

		pub fn inline_button(self, matchmaking_id: MatchmakingId, text: &str) -> teloxide::types::InlineKeyboardButton {
			teloxide::types::InlineKeyboardButton::new(
				text,
				teloxide::types::InlineKeyboardButtonKind::CallbackData(
					self.callback_data(matchmaking_id)
				)
			)
		}
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

	impl MatchmakingMessageTelegram {
		/// Get all the [MatchmakingMessageTelegram] for a specific [MatchmakingId].
		pub fn get_all(database: &mut PgConnection, matchmaking_id: MatchmakingId) -> AnyResult<Vec<Self>> {
			use diesel::prelude::*;
			use crate::interfaces::database::schema::matchmaking_messages_telegram;

			matchmaking_messages_telegram::table
				.filter(matchmaking_messages_telegram::matchmaking_id.eq(matchmaking_id.0))
				.get_results::<MatchmakingMessageTelegram>(database)
				.context("La query al database RYG è fallita.")
		}

		fn reply_markup(matchmaking_id: MatchmakingId) -> teloxide::types::InlineKeyboardMarkup {
			use MatchmakingTelegramKeyboardCallback::*;

			let button_yes = Yes.inline_button(matchmaking_id, "🔵 Ci sarò!");
			let button_5min = Plus5Min.inline_button(matchmaking_id, "🕐 +5 min");
			let button_15min = Plus15Min.inline_button(matchmaking_id, "🕒 +15 min");
			let button_60min = Plus60Min.inline_button(matchmaking_id, "🕛 +60 min");
			let button_maybe = Maybe.inline_button(matchmaking_id, "❔ Forse...");
			let button_dontw = DontWait.inline_button(matchmaking_id, "❓ Non aspettatemi.");
			let button_cant = Cant.inline_button(matchmaking_id, "🔺 Non posso...");
			let button_wont = Wont.inline_button(matchmaking_id, "🔻 Non mi interessa.");

			teloxide::types::InlineKeyboardMarkup::new(vec![
				vec![button_yes],
				vec![button_5min, button_15min, button_60min],
				vec![button_maybe, button_dontw],
				vec![button_cant, button_wont],
			])
		}

		fn text(event: &MatchmakingEvent, replies: &Vec<(MatchmakingReply, RoyalnetUser, TelegramUser)>) -> String {
			use std::fmt::Write;

			let mut result = String::new();

			let emoji = match event.has_started() {
				false => "🚩",
				true => "🔔",
			};

			let text = event.text.as_str().escape_telegram_html();
			writeln!(result, "{emoji} <b>{text}</b>").unwrap();

			let start = event.starts_at.format("%c").to_string().escape_telegram_html();
			writeln!(result, "<i>{start}</i>").unwrap();

			writeln!(result).unwrap();

			for (reply, royalnet, telegram) in replies {
				use MatchmakingChoice::*;

				let emoji = match reply.choice {
					Yes => "🔵",
					Late => match reply.late_mins {
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
					Maybe => "❔",
					DontWait => "❓",
					Cant => "🔺",
					Wont => "🔻",
				};

				let telegram_id = telegram.telegram_id.0;
				let username = &royalnet.username;

				write!(result, "{emoji} <a href=\"tg://user?id={telegram_id}\">{username}</a>").unwrap();

				if reply.choice == Late {
					let late_mins = reply.late_mins;

					write!(result, " (+{late_mins} mins)").unwrap();
				}

				writeln!(result).unwrap();
			}

			result
		}

		async fn send_new(
			database: &mut PgConnection,
			matchmaking_id: MatchmakingId,
			bot: &teloxide::Bot,
			chat_id: teloxide::types::ChatId,
			reply_to: Option<teloxide::types::MessageId>,
		) -> AnyResult<teloxide::types::Message> {
			let event = MatchmakingEvent::get(database, matchmaking_id)
				.context("Non è stato possibile recuperare il matchmaking dal database RYG.")?;

			let replies = MatchmakingReply::get_all_telegram(database, matchmaking_id)
				.context("Non è stato possibile recuperare le risposte al matchmaking dal database RYG.")?;

			let text = Self::text(&event, &replies);

			let mut request = bot.send_message(chat_id, text)
				.parse_mode(ParseMode::Html)
				.reply_markup(
					Self::reply_markup(matchmaking_id)
				);

			if let Some(reply_to) = reply_to {
				request = request.reply_parameters(
					teloxide::types::ReplyParameters::new(reply_to)
				);
			}

			request
				.await
				.context("La richiesta di invio messaggio alla Bot API di Telegram è fallita.")
		}

		fn create(
			database: &mut PgConnection,
			matchmaking_id: MatchmakingId,
			reply: &teloxide::types::Message,
		)
			-> AnyResult<Self>
		{
			use diesel::prelude::*;
			use diesel::dsl::*;
			use crate::interfaces::database::schema::matchmaking_messages_telegram;

			insert_into(matchmaking_messages_telegram::table)
				.values(&MatchmakingMessageTelegram {
					matchmaking_id,
					telegram_chat_id: reply.chat.id.into(),
					telegram_message_id: reply.id.into(),
				})
				.on_conflict_do_nothing()
				.get_result::<MatchmakingMessageTelegram>(database)
				.context("L'inserimento nel database RYG è fallito.")
		}

		pub async fn send_new_and_create(
			database: &mut PgConnection,
			matchmaking_id: MatchmakingId,
			bot: &teloxide::Bot,
			chat_id: teloxide::types::ChatId,
			reply_to: Option<teloxide::types::MessageId>,
		)
			-> AnyResult<Self>
		{
			let reply = Self::send_new(database, matchmaking_id, bot, chat_id, reply_to)
				.await
				.context("Non è stato possibile inviare il messaggio Telegram del matchmaking.")?;

			let this = Self::create(database, matchmaking_id, &reply)
				.context("Non è stato possibile aggiungere il messaggio Telegram al database RYG.")?;

			Ok(this)
		}

		async fn send_edit(
			&self,
			bot: &teloxide::Bot,
			text: &str,
			with_keyboard: bool,
		)
			-> AnyResult<teloxide::types::Message>
		{
			let telegram_chat_id: teloxide::types::ChatId = self.telegram_chat_id.into();

			let mut request = bot.edit_message_text(telegram_chat_id, self.telegram_message_id.into(), text)
				.parse_mode(ParseMode::Html);

			if with_keyboard {
				request = request.reply_markup(
					Self::reply_markup(self.matchmaking_id)
				)
			}

			request
				.await
				.context("La richiesta di modifica messaggio alla Bot API di Telegram è fallita.")
		}

		pub async fn make_text_and_send_edit(
			&self,
			database: &mut PgConnection,
			bot: &teloxide::Bot,
		)
			-> AnyResult<()>
		{
			let event = MatchmakingEvent::get(database, self.matchmaking_id)
				.context("Non è stato possibile recuperare il matchmaking dal database RYG.")?;

			let replies = MatchmakingReply::get_all_telegram(database, self.matchmaking_id)
				.context("Non è stato possibile recuperare le risposte al matchmaking dal database RYG.")?;

			let text = Self::text(&event, &replies);

			self.send_edit(bot, &text, !event.has_started())
				.await
				.context("Non è stato possibile modificare il messaggio Telegram del matchmaking.")?;

			Ok(())
		}

		async fn send_delete(
			&self,
			bot: &teloxide::Bot,
		)
			-> AnyResult<teloxide::types::True>
		{
			bot
				.delete_message::<teloxide::types::ChatId>(self.telegram_chat_id.into(), self.telegram_message_id.into())
				.await
				.context("La richiesta di eliminazione messaggio alla Bot API di Telegram è fallita.")
		}

		fn destroy(
			&self,
			database: &mut PgConnection,
		)
			-> AnyResult<usize>
		{
			use diesel::prelude::*;
			use diesel::dsl::*;
			use crate::interfaces::database::schema::matchmaking_messages_telegram;

			delete(matchmaking_messages_telegram::table)
				.filter(matchmaking_messages_telegram::matchmaking_id.eq(self.matchmaking_id))
				.filter(matchmaking_messages_telegram::telegram_chat_id.eq(self.telegram_chat_id))
				.filter(matchmaking_messages_telegram::telegram_message_id.eq(self.telegram_message_id))
				.execute(database)
				.context("La rimozione dal database RYG è fallita.")
		}

		pub async fn destroy_and_send_delete(
			self,
			database: &mut PgConnection,
			bot: &teloxide::Bot
		)
			-> AnyResult<()>
		{
			self.destroy(database)
				.context("Non è stato possibile eliminare il messaggio Telegram dal database RYG.")?;

			self.send_delete(bot)
				.await
				.context("Non è stato possibile eliminare il messaggio Telegram del matchmaking.")?;

			Ok(())
		}
	}
}