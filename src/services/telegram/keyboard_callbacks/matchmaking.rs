use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::AnswerCallbackQuerySetters;
use teloxide::requests::Requester;
use teloxide::types::CallbackQuery;

use crate::interfaces::database::models::{MatchmakingChoice, MatchmakingId, MatchmakingMessageTelegram, MatchmakingReply, RoyalnetUser};
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::services::telegram::keyboard_callbacks::KeyboardCallbackResult;
use crate::services::telegram::utils::matchmaking::MatchmakingTelegramKeyboardCallback;

pub async fn handler(bot: &Bot, query: CallbackQuery, matchmaking_id: MatchmakingId, callback: MatchmakingTelegramKeyboardCallback, database: &DatabaseInterface) -> KeyboardCallbackResult {
	use crate::services::telegram::utils::matchmaking::MatchmakingTelegramKeyboardCallback::*;
	
	let mut database = database.connect()
		.context("Non è stato possibile connettersi al database RYG.")?;
	
	let royalnet_user = RoyalnetUser::from_telegram_userid(&mut database, query.from.id)
		.context("Non è stato possibile recuperare il tuo utente Telegram dal database RYG.")?;
	
	match callback {
		Yes => MatchmakingReply::set(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Yes)?,
		Plus5Min => MatchmakingReply::add_late_minutes(&mut database, matchmaking_id, royalnet_user.id, 5)?,
		Plus15Min => MatchmakingReply::add_late_minutes(&mut database, matchmaking_id, royalnet_user.id, 15)?,
		Plus60Min => MatchmakingReply::add_late_minutes(&mut database, matchmaking_id, royalnet_user.id, 60)?,
		Maybe => MatchmakingReply::set(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Maybe)?,
		DontWait => MatchmakingReply::set(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::DontWait)?,
		Cant => MatchmakingReply::set(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Cant)?,
		Wont => MatchmakingReply::set(&mut database, matchmaking_id, royalnet_user.id, MatchmakingChoice::Wont)?,
	};
	
	let messages_telegram = MatchmakingMessageTelegram::get_all(&mut database, matchmaking_id)
		.context("Non è stato possibile recuperare i messaggi di matchmaking inviati su Telegram.")?;
	
	for message_telegram in messages_telegram {
		message_telegram.make_text_and_send_edit(&mut database, bot)
			.await
			.context("Non è stato possibile aggiornare un messaggio di matchmaking su Telegram.")?;
	}
	
	let _ = bot.answer_callback_query(query.id)
		.text("Ricevuto!")
		.await
		.context("Non è stato possibile rispondere alla pressione del bottone su Telegram.")?;
	
	Ok(())
}
