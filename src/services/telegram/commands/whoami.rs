use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message, ParseMode};
use crate::interfaces::database::models::RoyalnetUser;
use crate::services::telegram::dependencies::interface_database::DatabaseInterface;
use crate::utils::escape::TelegramEscape;
use super::CommandResult;

pub async fn handler(bot: &Bot, message: &Message, database: &DatabaseInterface) -> CommandResult {
	let author = message.from()
		.context("Non è stato possibile determinare chi ha inviato questo comando.")?;

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

	let username = &royalnet_user.username;

	let text = format!(
		"👤 Nel database RYG, tu hai l'username <code>{}</code>.",
		username.escape_telegram_html(),
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}
