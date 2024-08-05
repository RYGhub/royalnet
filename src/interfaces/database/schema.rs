// @generated automatically by Diesel CLI.

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
        context -> Text,
    }
}

diesel::table! {
    discord (discord_id) {
        user_id -> Int4,
        discord_id -> Int8,
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
diesel::joinable!(steam -> users (user_id));
diesel::joinable!(telegram -> users (user_id));

diesel::allow_tables_to_appear_in_same_query!(
    brooch_match,
    diario,
    discord,
    steam,
    telegram,
    users,
);
