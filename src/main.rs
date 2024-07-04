use anyhow::{Context, Result};

mod database;
mod telegram;

#[tokio::main]
async fn main() -> Result<()> {
    let mut tg = telegram::connect();

    teloxide::repl(tg, |tg: teloxide::Bot, msg: teloxide::types::Message| async move {
        use teloxide::prelude::*;

        let mut db = database::connect()
            .expect("Failed to connect to the database");

        let whoami = {
            use diesel::prelude::*;
            use database::schema::telegram::dsl::*;
            use database::models::*;
            telegram
                .filter(telegram_id.eq(msg.chat.id.0))
                .limit(1)
                .select(TelegramUser::as_select())
                .load(&mut db)
                .expect("Failed to query")
                .pop()
                .expect("Failed to get object")
        };

        tg.send_message(msg.chat.id, format!("{whoami:?}")).await?;
        Ok(())
    }).await;

    Ok(())
}
