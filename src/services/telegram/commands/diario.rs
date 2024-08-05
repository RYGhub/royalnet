use std::str::FromStr;
use anyhow::Context;
use once_cell::sync::Lazy;
use regex::Regex;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::Requester;
use teloxide::types::{Message, ParseMode};
use crate::interfaces::database::models::{DiarioAddition, DiarioEntry, RoyalnetUser};
use crate::services::telegram::commands::CommandResult;
use crate::services::telegram::deps::interface_database::DatabaseInterface;
use crate::utils::escape::EscapableInTelegramHTML;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiarioArgs {
	warning: Option<String>,
	quote: String,
	quoted: Option<String>,
	context: Option<String>,
}

impl FromStr for DiarioArgs {
	type Err = anyhow::Error;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		static REGEX: Lazy<Regex> = Lazy::new(|| Regex::new(r#" *(?:\[(?<warning>.+)])? *"(?<quote>.+)"[, ]*(?:[-–—]+(?<quoted>\w+)(?:, *(?<context>.+))?)?"#).unwrap());

		let captures = REGEX.captures(s)
			.context("Sintassi del comando incorretta.")?;

		let warning = captures.name("warning")
			.map(|s| s.as_str().to_owned());

		let quote = captures.name("quote")
			.context("Citazione non specificata nel comando.")?
			.as_str()
			.to_owned();

		let quoted = captures.name("quoted")
			.map(|s| s.as_str().to_owned());

		let context = captures.name("context")
			.map(|s| s.as_str().to_owned());

		Ok(
			Self { warning, quote, quoted, context }
		)
	}
}

pub fn stringify_entry(DiarioEntry { id, quoted_name, warning, quote, context, .. }: &DiarioEntry) -> String {
	let id = match warning {
		None => format!(
			"<code>#{}</code>",
			id,
		),
		Some(warning) => format!(
			"<code>#{}</code>, <b>{}</b>",
			id,
			warning.escape_telegram_html(),
		),
	};

	let quote = match warning {
		None => format!(
			"<blockquote>{}</blockquote>",
			quote.escape_telegram_html(),
		),
		Some(_) => format!(
			r#"<blockquote><span class="tg-spoiler">{}</span></blockquote>"#,
			quote.escape_telegram_html(),
		)
	};

	let cite = match (quoted_name, context) {
		(Some(name), Some(context)) => format!("—{name}, <i>{context}</i>"),
		(Some(name), None) => format!("—{name}"),
		(None, Some(context)) => format!("...<i>{context}</i>"),
		(None, None) => "".to_string(),
	};

	format!(
		"\
		{id}\n\
		{quote}\n\
		{cite}\
		"
	)
}

pub async fn handler(bot: &Bot, message: &Message, args: DiarioArgs, database: &DatabaseInterface) -> CommandResult {
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

	let addition = DiarioAddition {
		saver_id: Some(royalnet_user.id),
		warning: args.warning,
		quote: args.quote,
		quoted_name: args.quoted,
		context: args.context,
	};

	let entry = {
		use diesel::prelude::*;
		use diesel::dsl::*;
		use crate::interfaces::database::schema::diario::dsl::*;

		insert_into(diario)
			.values(&addition)
			.get_result::<DiarioEntry>(&mut database)
			.context("Non è stato possibile aggiungere la riga di diario al database RYG.")?
	};

	let entry = stringify_entry(&entry);

	let text = format!(
		"🖋 Riga aggiunta al diario!\n\
		\n\
		{entry}",
	);

	let _reply = bot
		.send_message(message.chat.id, text)
		.parse_mode(ParseMode::Html)
		.reply_to_message_id(message.id)
		.await
		// teloxide does not support blockquotes yet and errors out on parsing the response
		// .context("Non è stato possibile inviare la risposta.")?
		;

	Ok(())
}