use anyhow::{Context};
use rand::SeedableRng;
use rand::seq::SliceRandom;
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::{Message, Requester};
use crate::services::telegram::commands::{CommandResult};

// Cerchiamo di tenere bilanciate le tre colonne, o almeno le prime due.
// Se avete un'idea ma metterebbe troppe opzioni in un'unica categoria, mettetela sotto commento.
const ANSWERS: [&str; 60] = [
	// risposte "sì": 20
    "🔵 Sì.",
    "🔵 Decisamente sì!",
    "🔵 Uhm, secondo me sì.",
    "🔵 Sì! Sì! SÌ!",
    "🔵 Yup.",
    "🔵 Direi proprio di sì.",
    "🔵 Assolutamente sì.",
    "🔵 Ma certo!",
    "🔵 Esatto!",
    "🔵 Senz'altro!",
    "🔵 Ovviamente.",
    "🔵 Questa domanda ha risposta affermativa.",
    "🔵 Hell yeah.",
    "🔵 YES! YES! YES!",
    "🔵 yusssssss",
    "🔵 Non vedo perchè no",
    "🔵 Ha senso, ha perfettamente senso, nulla da obiettare, ha senso.",
    "🔵 Yos!",
    "🔵 Sì, ma tienilo segreto...",
    "🔵 [RADIO] Affermativo.",

    // risposte "no": 20
    "❌ No.",
    "❌ Decisamente no!",
    "❌ Uhm, secondo me sì. No, aspetta, ci ho ripensato. È un no.",
    "❌ No, no, e ancora NO!",
    "❌ Nope.",
    "❌ Direi proprio di no.",
    "❌ Assolutamente no.",
    "❌ Certo che no!",
    "❌ Neanche per idea!",
    "❌ Neanche per sogno!",
    "❌ Niente affatto!",
    "❌ Questa domanda ha risposta negativa.",
    "❌ Hell no.",
    "❌ NO! NO! NO!",
    "❌ lolno",
    "❌ NEIN NEIN NEIN NEIN",
    "❌ Delet dis",
    "❌ Nopety nope!",
    "❌ No, ma tienilo segreto.",
    "❌ [RADIO] Negativo.",

    // risposte "boh": 20
    "❔ Boh.",
    "❔ E io che ne so?!",
    "❔ Non so proprio rispondere.",
    "❔ Non lo so...",
    "❔ Mi avvalgo della facoltà di non rispondere.",
    "❔ Non parlerò senza il mio avvocato!",
    "❔ Dunno.",
    "❔ Perché lo chiedi a me?",
    "❔ Ah, non lo so io!",
    r#"❔ ¯\_(ツ)_/¯"#,
    "❔ No idea.",
    "❔ Dunno.",
    "❔ Boooooh!",
    "❔ Non ne ho la più pallida idea.",
    "❔ No comment.",
    "❔ maibi",
    "❔ maibi not",
    "❔ idk dude",
    "❔ Non mi è permesso condividere questa informazione.",
    "❔ [RADIO] Mantengo la posizione.",
];

pub async fn handler(bot: &Bot, message: &Message) -> CommandResult {
	let mut rng = rand::rngs::SmallRng::from_entropy();

	let answer = ANSWERS.choose(&mut rng)
		.context("Non è stato possibile selezionare una risposta.")?;

	let _reply = bot
		.send_message(message.chat.id, answer.to_string())
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}