use anyhow::Context;
use reqwest::Url;
use teloxide::Bot;
use teloxide::payloads::SendPhotoSetters;
use teloxide::requests::Requester;
use teloxide::types::{InputFile, Message, ReplyParameters};
use serde::Deserialize;
use super::{CommandResult};


const CAT_API_URL: &str = "https://api.thecatapi.com/v1/images/search";

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
struct CatQueryResponse {
	// id: String,
	pub url: String,
	// width: usize,
	// height: usize,
}


pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let response = reqwest::get(CAT_API_URL).await
		.context("Non è stato possibile richiedere un gatto all'API.")?
		.json::<Vec<CatQueryResponse>>().await
		.context("Il gatto ricevuto in risposta dall'API è indecifrabile, quindi non è stato possibile riceverlo.")?
		.pop()
		.context("Il gatto ricevuto in risposta dall'API non esiste, quindi non è stato possibile riceverlo.")?;

	let url: Url = response.url.parse()
		.context("L'URL del gatto ricevuto in risposta dall'API è malformato, quindi non è stato possibile riceverlo.")?;

	let input = InputFile::url(url);

	let _reply = bot
		.send_photo(message.chat.id, input)
		.reply_parameters(ReplyParameters::new(message.id))
		.await
		.context("Non è stato possibile inviare un gatto in risposta a questo messaggio.")?;

	Ok(())
}
