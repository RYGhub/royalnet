use micronfig::config;

// Everything ok, RustRover?
config! {
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_NOTIFICATION_CHATID?: String > i64 -> ChatIdConversionHack -> teloxide::types::ChatId,
}

struct ChatIdConversionHack(i64);

impl From<i64> for ChatIdConversionHack {
    fn from(value: i64) -> Self {
        Self(value)
    }
}

impl From<ChatIdConversionHack> for teloxide::types::ChatId {
    fn from(value: ChatIdConversionHack) -> Self {
        Self(value.0)
    }
}
