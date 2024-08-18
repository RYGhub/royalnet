// @generated automatically by Diesel CLI.

pub mod sql_types {
    #[derive(diesel::query_builder::QueryId, Clone, diesel::sql_types::SqlType)]
    #[diesel(postgres_type(name = "matchmaking_choice"))]
    pub struct MatchmakingChoice;
}

diesel::table! {
    brooch_match (id) {
        id -> Int8,
    }
}

diesel::table! {
    diario (id) {
        id -> Int4,
        saver_id -> Nullable<Int4>,
        saved_on -> Nullable<Timestamp>,
        quoted_id -> Nullable<Int4>,
        quoted_name -> Nullable<Varchar>,
        warning -> Nullable<Text>,
        quote -> Text,
        context -> Nullable<Text>,
    }
}

diesel::table! {
    discord (discord_id) {
        user_id -> Int4,
        discord_id -> Int8,
    }
}

diesel::table! {
    matchmaking_events (id) {
        id -> Int4,
        text -> Varchar,
        starts_at -> Timestamp,
    }
}

diesel::table! {
    matchmaking_messages_telegram (matchmaking_id, telegram_chat_id, telegram_message_id) {
        matchmaking_id -> Int4,
        telegram_chat_id -> Int8,
        telegram_message_id -> Int4,
    }
}

diesel::table! {
    use diesel::sql_types::*;
    use super::sql_types::MatchmakingChoice;

    matchmaking_replies (matchmaking_id, user_id) {
        matchmaking_id -> Int4,
        user_id -> Int4,
        choice -> MatchmakingChoice,
        late_mins -> Int4,
    }
}

diesel::table! {
    steam (steam_id) {
        user_id -> Int4,
        steam_id -> Int8,
    }
}

diesel::table! {
    telegram (telegram_id) {
        user_id -> Int4,
        telegram_id -> Int8,
    }
}

diesel::table! {
    users (id) {
        id -> Int4,
        username -> Varchar,
    }
}

diesel::joinable!(discord -> users (user_id));
diesel::joinable!(matchmaking_messages_telegram -> matchmaking_events (matchmaking_id));
diesel::joinable!(matchmaking_replies -> matchmaking_events (matchmaking_id));
diesel::joinable!(matchmaking_replies -> users (user_id));
diesel::joinable!(steam -> users (user_id));
diesel::joinable!(telegram -> users (user_id));

diesel::allow_tables_to_appear_in_same_query!(
    brooch_match,
    diario,
    discord,
    matchmaking_events,
    matchmaking_messages_telegram,
    matchmaking_replies,
    steam,
    telegram,
    users,
);
