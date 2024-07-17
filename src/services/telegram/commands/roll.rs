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

	let captures = re.captures(roll)
		.context("Sintassi dei dadi non corretta.")?;
	
	let qty = captures.name("qty")
		.map(|m| m.as_str())
		.map(|m| m.parse::<u32>())
		.unwrap_or(Ok(1))
		.context("La quantità di dadi da lanciare deve essere un numero intero positivo diverso da 0.")?;

	let die = captures.name("die")
		.unwrap()
		.as_str()
		.parse::<u32>()
		.context("La dimensione del dado da lanciare deve essere un numero intero positivo.")?;

	let modifier = captures.name("modifier")
		.map(|m| m.as_str())
		.map(|m| m.parse::<i32>())
		.unwrap_or(Ok(0))
		.context("Il modificatore dei dadi lanciati deve essere un numero intero.")?;

    if die == 0  {
		anyhow::bail!("Non è stato specificato nessun dado.")
    }

    if qty < 1  {
        anyhow::bail!("La quantità di dadi specificata deve essere un intero positivo.")
    }

    let mut nums_rolled = Vec::<u32>::new();
    for _ in 0..qty {
        nums_rolled.push(
			rng.gen_range(1..=die)
		);
    }
	
	let roll_string = nums_rolled
		.iter()
		.map(|n| n.to_string())
		.collect::<Vec<String>>()
		.join("\n");
        
    let mut answer = format!("🎲 [{roll_string}]");
		
    if modifier != 0 {
		answer.push_str(&format!("{modifier:+}"))
    }

    answer.push_str(" = ");

    let sum: u32 = nums_rolled.iter().sum();
    let sum: i32 = sum as i32 + modifier;
	
    answer.push_str(&sum.to_string());
	
	let _reply = bot
		.send_message(message.chat.id, answer)
		.reply_to_message_id(message.id)
		.await
		.context("Non è stato possibile inviare la risposta.")?;

	Ok(())
}