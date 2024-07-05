use anyhow::Error;
use teloxide::{Bot, dptree};
use teloxide::dispatching::{DefaultKey, Dispatcher, HandlerExt, UpdateFilterExt};
use teloxide::dispatching::dialogue::{InMemStorage, TraceStorage};
use teloxide::types::{Message, Update};

mod start;
mod fortune;

#[derive(Debug, Clone, Default)]
enum State {
	#[default]
	Default,
}

type CommandDialogue = teloxide::dispatching::dialogue::Dialogue<State, TraceStorage<InMemStorage<State>>>;
type CommandResult = anyhow::Result<()>;

async fn detect_command(bot: Bot, dialogue: CommandDialogue, message: Message) -> CommandResult {
	let text = message.text();
	if text.is_none() {
		// Ignore non-textual messages
		return Ok(())
	}
	let text = text.unwrap();

	match text {
		"/start" => start::handler(bot, dialogue, message).await,
		"/fortune" => fortune::handler(bot, dialogue, message).await,
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
