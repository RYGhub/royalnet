// See the following link for an example of how to use this file:
// https://github.com/teloxide/teloxide/blob/master/crates/teloxide/examples/dispatching_features.rs

use std::sync::Arc;
use anyhow::{Context, Error};
use teloxide::{Bot, dptree};
use teloxide::dispatching::{DefaultKey, Dispatcher, HandlerExt, UpdateFilterExt};
use teloxide::dptree::entry;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{Message, Update};
use teloxide::utils::command::BotCommands;

mod start;
mod fortune;

#[derive(Debug, Clone, BotCommands)]
#[command(rename_rule = "lowercase")]
enum Command {
	Start,
	Fortune,
}

async fn handle_command(bot: Bot, command: Command, message: Message) -> CommandResult {
	log::trace!("Received command: {command:?}");

	match command {
		Command::Start => start::handler(bot, message).await,
		Command::Fortune => fortune::handler(bot, message).await,
	}
}

async fn unknown_command(bot: Bot, message: Message) -> CommandResult {
	log::trace!("Received an unknown command.");

	bot.send_message(message.chat.id, "⚠️ Comando sconosciuto.")
		.reply_to_message_id(message.id)
		.await
		.context("Failed to send message")?;

	Ok(())
}

pub fn dispatcher(bot: Bot) -> Dispatcher<Bot, Error, DefaultKey> {
	Dispatcher::builder(
		bot,
		Update::filter_message()
			.branch(
				entry()
					.filter_command::<Command>()
					.endpoint(handle_command)
			)
			.endpoint(unknown_command)
	)
		.dependencies(
			dptree::deps![]  // No deps needed at the moment.
		)
		.enable_ctrlc_handler()
		.build()
}

type CommandResult = anyhow::Result<()>;