// @generated automatically by Diesel CLI.

pub mod sql_types {
    #[derive(Debug, Clone, diesel::sql_types::SqlType)]
    #[diesel(postgres_type(name = "matchmaking_reply"))]
    pub struct MatchmakingReplyType;
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
    use diesel::sql_types::*;
    use super::sql_types::MatchmakingReplyType;

    matchmade (matchmaking_id, user_id) {
        matchmaking_id -> Int4,
        user_id -> Int4,
        reply -> MatchmakingReplyType,
        late_mins -> Int4,
    }
}

diesel::table! {
    matchmaking (id) {
        id -> Int4,
        text -> Varchar,
        starts_at -> Timestamp,
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
diesel::joinable!(matchmade -> matchmaking (matchmaking_id));
diesel::joinable!(matchmade -> users (user_id));
diesel::joinable!(steam -> users (user_id));
diesel::joinable!(telegram -> users (user_id));

diesel::allow_tables_to_appear_in_same_query!(
    brooch_match,
    diario,
    discord,
    matchmade,
    matchmaking,
    steam,
    telegram,
    users,
);
