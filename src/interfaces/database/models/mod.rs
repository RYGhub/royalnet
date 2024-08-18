use std::io::Write;

use diesel::deserialize::FromSql;
use diesel::serialize::ToSql;

pub mod users;
pub mod telegram;
pub mod discord;
pub mod steam;
pub mod brooch_match;
pub mod diario;
pub mod matchmaking_events;
pub mod matchmaking_replies;
pub mod matchmaking_messages_telegram;
pub mod matchmaking_choice;
