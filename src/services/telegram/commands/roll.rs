use anyhow::{Context};
use rand::{Rng, SeedableRng};
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::{Message, Requester};
use crate::services::telegram::commands::{CommandResult};
use regex::Regex;



pub async fn handler(bot: &Bot, message: &Message, roll: &str) -> CommandResult {
    let mut rng = rand::rngs::SmallRng::from_entropy();
    if rng.gen_range(1..1001) == 1 {
        let _reply = bot
		.send_message(message.chat.id, "🎶 Roll? Rick roll! https://www.youtube.com/watch?v=dQw4w9WgXcQ")
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	    return Ok(())
    }

    let re = Regex::new(r#"(?P<qty>[0-9]*)?d(?P<die>[0-9]+)(?P<modifier>[+-]?[0-9]*)?"#).unwrap();
let qty = captures.name("qty") // Prova a vedere se c'è il gruppo "qty"
		.map(|m| m.as_str())  // `map`: se c'è, trasforma il suo contenuto in stringa
		.map(|m| m.parse::<u32>())  // `map`: se c'è, trasforma la stringa in un u32
		.map(|m| m.context("La quantità di dadi da lanciare deve essere un numero intero positivo diverso da 0.")?)  // `map`: se c'è, ma il parsing ha dato errore, restituiscilo e fai terminare la funzione qui
		.unwrap_or(1);  // `unwrap_or`: se c'è, restituisci il valore, altrimenti, defaulta a 1

	let die = captures.name("die") // Prova a vedere se c'è il gruppo "die"
		.unwrap()  // `unwrap`: possiamo asserire che il gruppo "die" sia sempre presente se la regex ha matchato
		.as_str()  // trasforma il suo contenuto in stringa
		.parse::<u32>()  // trasforma la stringa in un u32
		.context("La dimensione del dado da lanciare deve essere un numero intero positivo.")?;  // se il parsing ha dato errore, restituiscilo e fai terminare la funzione qui

	let modifier = captures.name("modifier") // Prova a vedere se c'è il gruppo "modifier"
		.map(|m| m.as_str())  // `map`: se c'è, trasforma il suo contenuto in stringa
		.map(|m| m.parse::<i32>())  // `map`: se c'è, trasforma la stringa in un i32
		.map(|m| m.context("Il modificatore dei dadi lanciati deve essere un numero intero.")?)  // `map`: se c'è, ma il parsing ha dato errore, restituiscilo e fai terminare la funzione qui
		.unwrap_or(0);  // `unwrap_or`: se c'è, restituisci il valore, altrimenti, defaulta a 0

    if die <= 0  {
		anyhow::bail!("Non è stato specificato nessun dado.")
    }

    if qty < 1  {
        anyhow::bail!("La quantità di dadi specificata deve essere un intero positivo.")
    }



    let mut nums_rolled = Vec::<i32>::new();
    for _ in 0..qty {
        nums_rolled.push(rng.gen_range(1..die+1));
    }
    
    
    let mut answer = String::from("🎲 [");
    for i in 0..qty {
        if i > 0 { answer.push_str("+")}
        answer.push_str( &nums_rolled[i].to_string() );
    }
    answer.push_str("] ");

    if modifier != 0 {
        if modifier > 0 {
            answer.push_str("+");
        }
        answer.push_str( &modifier.to_string() );
    }

    answer.push_str(" = ");

    let mut sum: i32 = nums_rolled.iter().sum();
    sum = sum + modifier;


    answer.push_str( &sum.to_string() );


	let _reply = bot
		.send_message(message.chat.id, answer)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}