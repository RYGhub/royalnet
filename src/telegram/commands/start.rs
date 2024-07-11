use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use super::{CommandResult};


const VERSION: &str = env!("CARGO_PKG_VERSION");


pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let author = message.from()
		.context("Non è stato possibile determinare chi ha inviato questo comando.")?;

	let author_username = match author.username.as_ref() {
		None => {
			author.first_name.clone()
		},
		Some(username) => {
			format!("@{}", &username)
		},
	};

	let me = bot
		.get_me()
		.await
		.context("Non è stato possibile recuperare informazioni sul bot.")?;

	let me_username = me.username.as_ref()
		.context("Non è stato possibile determinare l'username del bot.")?;

	let text = format!(
		"👋 Ciao {author_username}! Sono @{me_username}, il robot tuttofare della RYG!\n\n\
		Sto eseguendo la versione {VERSION}.\n\n\
		Puoi vedere l'elenco delle mie funzionalità dal menu in basso.\n\n\
		Cosa posso fare per te oggi?",
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}
