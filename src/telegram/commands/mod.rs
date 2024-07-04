use anyhow::Error;
use diesel::PgConnection;
use teloxide::{Bot, dptree};
use teloxide::dispatching::{DefaultKey, Dispatcher, HandlerExt, UpdateFilterExt};
use teloxide::dispatching::dialogue::{InMemStorage, TraceStorage};
use teloxide::types::{Message, Update};
use teloxide::utils::command::BotCommands;

mod start;

#[derive(Debug, Clone, Default)]
enum State {
	#[default]
	Default,
}

type Dialogue = teloxide::dispatching::dialogue::Dialogue<State, TraceStorage<InMemStorage<State>>>;
type Result = anyhow::Result<()>;

async fn detect_command(bot: Bot, dialogue: Dialogue, message: Message) -> Result {
	let text = message.text();
	if text.is_none() {
		// Ignore non-textual messages
		return Ok(())
	}
	let text = text.unwrap();

	match text {
		"/start" => start::handler(bot, dialogue, message).await,
		_ => anyhow::bail!("Unknown command"),
	}
}

pub(super) fn dispatcher(bot: Bot) -> Dispatcher<Bot, Error, DefaultKey> {
	Dispatcher::builder(
		bot,
		Update::filter_message()
			.enter_dialogue::<Message, TraceStorage<InMemStorage<State>>, State>()
			.branch(
				dptree::case![State::Default]
					.endpoint(detect_command)
			)
	)
		.dependencies(
			dptree::deps![
				TraceStorage::new(
					InMemStorage::<State>::new()
				)
			]
		)
		.enable_ctrlc_handler()
		.build()
}
