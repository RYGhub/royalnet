use anyhow::Context;
use diesel::PgConnection;
use teloxide::Bot;
use teloxide::payloads::AnswerCallbackQuerySetters;
use teloxide::requests::Requester;
use teloxide::types::CallbackQuery;
use crate::interfaces::database::models::matchmaking_choice::MatchmakingChoice;
use crate::interfaces::database::models::matchmaking_messages_telegram::MatchmakingMessageTelegram;
use crate::interfaces::database::models::matchmaking_replies::MatchmakingReply;
use crate::interfaces::database::models::users::RoyalnetUser;
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::services::telegram::keyboard_callbacks::KeyboardCallbackResult;
use crate::services::telegram::utils::matchmaking::MatchmakingTelegramKeyboardCallback;
use crate::utils::result::AnyResult;

pub async fn handler(bot: &Bot, query: CallbackQuery, matchmaking_id: i32, callback: MatchmakingTelegramKeyboardCallback, database: &DatabaseInterface) -> KeyboardCallbackResult {
	let mut database = database.connect()
		.context("Non è stato possibile connettersi al database RYG.")?;

	let royalnet_user = RoyalnetUser::from_telegram_userid(&mut database, query.from.id)
		.context("Non è stato possibile recuperare il tuo utente Telegram dal database RYG.")?;

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


impl MatchmakingTelegramKeyboardCallback {
	fn handle(database: &mut PgConnection, matchmaking_id ) -> AnyResult<MatchmakingReply> {
		
	}
}