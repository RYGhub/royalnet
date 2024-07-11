use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use crate::database::models::{RoyalnetUser};
use super::{CommandResult};

pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let author = message.from()
		.context("Non è stato possibile determinare chi ha inviato questo comando.")?;

	let mut database = crate::database::connect().
		context("Non è stato possibile connettersi al database RYG.")?;

	let royalnet_user: RoyalnetUser = {
		use diesel::prelude::*;
		use diesel::{ExpressionMethods, QueryDsl};
		use crate::database::schema::telegram::dsl::*;
		use crate::database::schema::users::dsl::*;
		use crate::database::models::RoyalnetUser;

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
		"👤 Nel database RYG, tu hai l'username «{username}»."
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}
