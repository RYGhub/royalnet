use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message, ReplyParameters};
use super::{CommandResult};

pub async fn handler(bot: &Bot, message: &Message, text: &str) -> CommandResult {
	let text = format!(
		"💬 {text}"
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}
