use anyhow::{Context};
use rand::{Rng, SeedableRng};
use teloxide::Bot;
use teloxide::payloads::SendMessageSetters;
use teloxide::prelude::{Message, Requester};
use crate::services::telegram::commands::{CommandResult};
use regex::Regex;



pub async fn handler(bot: &Bot, message: &Message, roll: &str) -> CommandResult {
    let re = Regex::new(r#"(?P<qty>[0-9]*)?d(?P<die>[0-9]+)(?P<mod>[+-][0-9]+)?"#);
    let mut rng = rand::rngs::SmallRng::from_entropy();
    let mut qty = 1;
    let mut die = 20;
    let mut modifier = 0;

    match re?.captures(roll) {
        Some(caps) => {
            qty = caps["qty"].parse()?;
            die = caps["die"].parse()?;
            modifier = caps["mod"].parse()?;
        }
        None => {}
    }
    

    let mut nums_rolled = Vec::<i32>::new();
    for _i in 0..qty {
        nums_rolled.push(rng.gen_range(1..die));
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