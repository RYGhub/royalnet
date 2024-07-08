use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use super::{CommandResult};

pub async fn handler(bot: Bot, message: Message, text: String) -> CommandResult {
	let text = format!(
		"💬 {text}"
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Failed to send message")?;

	Ok(())
}
