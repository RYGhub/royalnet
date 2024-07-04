use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use super::{Dialogue, Result};

pub(super) async fn handler(bot: Bot, _dialogue: Dialogue, message: Message) -> Result {
	let author = message.from()
		.context("Failed to get the user who sent the original message")?;

	let author_username = match author.username.as_ref() {
		None => {
			format!("{}", &author.first_name)
		},
		Some(username) => {
			format!("@{}", &username)
		},
	};

	let me = bot
		.get_me()
		.await
		.context("Failed to get information about self")?;

	let me_username = me.username.as_ref()
		.context("Failed to get bot's username")?;

	let text = format!(
		"👋 Ciao {author_username}! Sono @{me_username}, il robot tuttofare della RYG!\n\n\
		Puoi vedere l'elenco delle mie funzionalità dal menu in basso.\n\n\
		Cosa posso fare per te oggi?"
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Failed to send message")?;

	Ok(())
}
