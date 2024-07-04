// @generated automatically by Diesel CLI.

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
    discord,
    steam,
    telegram,
    users,
);
