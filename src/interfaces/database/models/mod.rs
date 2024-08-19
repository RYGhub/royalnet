#![allow(unused_imports)]

use std::io::Write;

use diesel::deserialize::FromSql;
use diesel::serialize::ToSql;

pub use brooch_match::{BroochMatch, DotaMatchId};
pub use diario::Diario;
pub use matchmaking_choice::MatchmakingChoice;
pub use matchmaking_events::{MatchmakingEvent, MatchmakingId};
pub use matchmaking_messages_telegram::MatchmakingMessageTelegram;
pub use matchmaking_replies::MatchmakingReply;
pub use telegram::{TelegramUser, TelegramUserId};
pub use users::{RoyalnetUser, RoyalnetUserId};

mod users;
mod telegram;
mod discord;
mod steam;
mod brooch_match;
mod diario;
mod matchmaking_events;
mod matchmaking_replies;
mod matchmaking_messages_telegram;
mod matchmaking_choice;

