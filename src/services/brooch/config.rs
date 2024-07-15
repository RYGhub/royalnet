use micronfig::config;

config! {
	BROOCH_WATCHED_GUILD_ID: String > i64 -> crate::stratz::GuildId,
	BROOCH_NOTIFICATION_CHAT_ID: String > i64 -> crate::utils::hacks::ChatIdConversionHack -> teloxide::types::ChatId
}