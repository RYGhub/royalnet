use anyhow::Context;
use reqwest::Url;
use teloxide::Bot;
use teloxide::payloads::SendPhotoSetters;
use teloxide::requests::Requester;
use teloxide::types::{InputFile, Message};
use serde::Deserialize;
use super::{CommandResult};


const DOG_API_URL: &str = "https://dog.ceo/api/breeds/image/random";

#[derive(Debug, Clone, PartialEq, Eq, Deserialize)]
struct DogQueryResponse {
	// status: String,
	pub message: String,
}


pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let response = reqwest::get(DOG_API_URL).await
		.context("Non è stato possibile richiedere un cane all'API.")?
		.json::<DogQueryResponse>().await
		.context("Il cane ricevuto in risposta dall'API è indecifrabile, quindi non è stato possibile riceverlo.")?;

	let url: Url = response.message.parse()
		.context("L'URL del cane ricevuto in risposta dall'API è malformato, quindi non è stato possibile riceverlo.")?;

	let input = InputFile::url(url);

	let _reply = bot
		.send_photo(message.chat.id, input)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare un cane in risposta a questo messaggio.")?;

	Ok(())
}