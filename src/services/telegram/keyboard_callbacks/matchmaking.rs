use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::AnswerCallbackQuerySetters;
use teloxide::requests::Requester;
use teloxide::types::CallbackQuery;
use crate::interfaces::database::models::{MatchmakingChoice, MatchmakingMessageTelegram, MatchmakingReply, RoyalnetUser};
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::services::telegram::keyboard_callbacks::KeyboardCallbackResult;
use crate::services::telegram::utils::matchmaking::MatchmakingTelegramKeyboardCallback;

pub async fn handler(bot: &Bot, query: CallbackQuery, matchmaking_id: i32, callback: &MatchmakingTelegramKeyboardCallback, database: &DatabaseInterface) -> KeyboardCallbackResult {
	log::info!("{:?}", &callback);

	let author = query.from;

	let mut database = database.connect()?;

	let royalnet_user: RoyalnetUser = {
		use diesel::prelude::*;
		use diesel::{ExpressionMethods, QueryDsl};
		use crate::interfaces::database::schema::telegram::dsl::*;
		use crate::interfaces::database::schema::users::dsl::*;
		use crate::interfaces::database::models::RoyalnetUser;

		telegram
			.filter(telegram_id.eq::<i64>(
				author.id.0.try_into()
					.context("Non è stato possibile processare il tuo ID Telegram per via di un overflow.")?
			))
			.inner_join(users)
			.select(RoyalnetUser::as_select())
			.get_result(&mut database)
			.context("Non è stato possibile recuperare il tuo utente Telegram dal database RYG.")?
	};

	match callback {
		MatchmakingTelegramKeyboardCallback::Yes => {
			MatchmakingReply::put(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Yes)?;
		}
		MatchmakingTelegramKeyboardCallback::Plus5Min => {
			MatchmakingReply::put_delay(&mut database, matchmaking_id, royalnet_user.id, 5)?;
		}
		MatchmakingTelegramKeyboardCallback::Plus15Min => {
			MatchmakingReply::put_delay(&mut database, matchmaking_id, royalnet_user.id, 15)?;
		}
		MatchmakingTelegramKeyboardCallback::Plus60Min => {
			MatchmakingReply::put_delay(&mut database, matchmaking_id, royalnet_user.id, 60)?;
		}
		MatchmakingTelegramKeyboardCallback::Maybe => {
			MatchmakingReply::put(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Maybe)?;
		}
		MatchmakingTelegramKeyboardCallback::DontWait => {
			MatchmakingReply::put(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::DontWait)?;
		}
		MatchmakingTelegramKeyboardCallback::Cant => {
			MatchmakingReply::put(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Cant)?;
		}
		MatchmakingTelegramKeyboardCallback::Wont => {
			MatchmakingReply::put(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Wont)?;
		}
	}

	MatchmakingMessageTelegram::update_all(&mut database, matchmaking_id, bot)
		.await?;

	let _ = bot.answer_callback_query(query.id)
		.text("Ricevuto!")
		.await?;

	Ok(())
}
