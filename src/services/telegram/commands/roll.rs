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

    let re = Regex::new(r#"(?P<qty>[0-9]*)?d(?P<die>[0-9]+)(?P<modifier>[+-]?[0-9]*)?"#);
    let mut qty = 1;
    let mut die = 0;
    let mut modifier = 0;

    match re?.captures(roll) {
        Some(caps) => {
            qty = caps["qty"].parse().unwrap_or(qty);
            die = caps["die"].parse().unwrap_or(die);
            modifier = caps["modifier"].parse().unwrap_or(modifier);
        }
        None => {}
    }

    if die <= 0  {
        let _reply = bot
		.send_message(message.chat.id, "Specificare almeno un dado.")
		.reply_to_message_id(message.id)
		.await
		.context("Dado = 0")?;

	    return Ok(())
    }

    if qty < 1  {
        let _reply = bot
		.send_message(message.chat.id, "La quantità di dadi da tirare deve essere un intero positivo. (lasciare vuoto per sottintendere 1)")
		.reply_to_message_id(message.id)
		.await
		.context("Qty < 1")?;

	    return Ok(())
    }



    let mut nums_rolled = Vec::<i32>::new();
    for _i in 0..qty {
        nums_rolled.push(rng.gen_range(1..die+1));
    }
    
    
    let mut answer: String = "🎲 [".to_string();
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