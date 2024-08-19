#![allow(unused_attributes, unused_qualifications, clippy::needless_pub_self)]


#[cfg(feature = "interface_database")]
pub mod interface_database {
	use micronfig::config;
	
	config! {
		DATABASE_AUTOMIGRATE: String > bool,
		DATABASE_URL: String,
	}
}

#[cfg(feature = "service_telegram")]
pub mod service_telegram {
	use micronfig::config;
	
	config! {
		TELEGRAM_DATABASE_URL: String,
		TELEGRAM_BOT_TOKEN: String,
		TELEGRAM_NOTIFICATION_CHATID?: String > i64 -> crate::instance::config::ChatIdConversionHack -> teloxide::types::ChatId,
	}
}

#[cfg(feature = "service_brooch")]
pub mod brooch {
	use micronfig::config;
	
	#[allow(unused_qualifications)]
	config! {
		BROOCH_DATABASE_URL: String,
		BROOCH_GRAPHQL_URL: String,
		BROOCH_STRATZ_TOKEN: String,
		BROOCH_TELEGRAM_BOT_TOKEN: String,
		BROOCH_WATCHED_GUILD_ID: String > i64,
		BROOCH_MIN_PLAYERS_TO_PROCESS: String > usize,
		BROOCH_NOTIFICATION_CHAT_ID: String > i64 -> crate::instance::config::ChatIdConversionHack -> teloxide::types::ChatId,
		BROOCH_MAX_IMP_WAIT_SECS: String > i64 -> crate::instance::config::TimeDeltaConversionHack => chrono::TimeDelta,
	}
}

#[cfg(feature = "service_telegram")]
pub struct ChatIdConversionHack(i64);

#[cfg(feature = "service_telegram")]
impl From<i64> for ChatIdConversionHack {
	fn from(value: i64) -> Self {
		Self(value)
	}
}

#[cfg(feature = "service_telegram")]
impl From<ChatIdConversionHack> for teloxide::types::ChatId {
	fn from(value: ChatIdConversionHack) -> Self {
		Self(value.0)
	}
}

pub struct TimeDeltaConversionHack(i64);

impl From<i64> for TimeDeltaConversionHack {
	fn from(value: i64) -> Self {
		Self(value)
	}
}

impl TryFrom<TimeDeltaConversionHack> for chrono::TimeDelta {
	type Error = ();
	
	fn try_from(value: TimeDeltaConversionHack) -> Result<Self, Self::Error> {
		Self::new(value.0, 0).ok_or(())
	}
}