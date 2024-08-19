use anyhow::Context;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::requests::Requester;
use teloxide::types::{BotCommand, Message, ParseMode, ReplyParameters};
use teloxide::utils::command::BotCommands;

use super::CommandResult;

pub async fn handler_all(bot: &Bot, message: &Message) -> CommandResult {
	let descriptions = super::Command::descriptions().to_string();

	let text = format!("❔ <b>Comandi disponibili</b>\n\n{descriptions}");

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}

pub async fn handler_specific(bot: &Bot, message: &Message, target: &str) -> CommandResult {
	let me = bot
		.get_me()
		.await
		.context("Non è stato possibile recuperare informazioni sul bot.")?;

	let me_username = me.username.as_ref()
		.context("Non è stato possibile determinare l'username del bot.")?;

	let suffix = format!("@{me_username}");

	let target = target.strip_prefix('/')
		.unwrap_or(target);

	let target = target.strip_suffix(&suffix)
		.unwrap_or(target);

	log::trace!("Stripped target command: {target:?}");

	let all_commands: Vec<BotCommand> = super::Command::bot_commands();

	log::trace!("All commands are: {all_commands:?}");

	let identify_command = |cmd: &&BotCommand| -> bool {
		let command = &cmd.command;

		let command = command.strip_prefix('/')
			.unwrap_or_else(|| command);

		target == command
	};

	let target = match all_commands.iter().find(identify_command) {
		Some(bot_command) => bot_command,
		None => anyhow::bail!("Non è stato possibile trovare il comando specificato."),
	};

	let display_suffix = match message.chat.is_private() {
		false => &suffix,
		true => "",
	};

	let text = format!("❔ <b>Comando {}{}</b>\n\n{}", target.command, display_suffix, target.description);

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}