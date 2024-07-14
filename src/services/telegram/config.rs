use micronfig::config;

// Everything ok, RustRover?
config! {
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_NOTIFICATION_CHATID?: String > i64 -> crate::utils::hacks::ChatIdConversionHack -> teloxide::types::ChatId,
}
