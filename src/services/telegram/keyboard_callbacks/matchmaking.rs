use teloxide::Bot;
use teloxide::prelude::CallbackQuery;
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::services::telegram::keyboard_callbacks::KeyboardCallbackResult;
use crate::services::telegram::utils::matchmaking::MatchmakingTelegramKeyboardCallback;

pub async fn handler(_bot: &Bot, query: CallbackQuery, matchmaking_id: i32, callback: &MatchmakingTelegramKeyboardCallback, _database: &DatabaseInterface) -> KeyboardCallbackResult {
	log::info!("{:?}", &callback);

	Ok(())
}
