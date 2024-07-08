use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message};
use teloxide::utils::command::BotCommands;
use super::{CommandResult};

pub async fn handler(bot: Bot, message: Message) -> CommandResult {
	let descriptions = super::Command::descriptions().to_string();

	let text = format!("❓ Sono disponibili i seguenti comandi:\n\n{descriptions}");

	let _reply = bot
		.send_message(message.chat.id, text)
		.reply_to_message_id(message.id)
		.await
		.context("Failed to send message")?;

	Ok(())
}
