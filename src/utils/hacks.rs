use teloxide::types::ChatId;

pub struct ChatIdConversionHack(i64);

impl From<i64> for ChatIdConversionHack {
	fn from(value: i64) -> Self {
		Self(value)
	}
}

impl From<ChatIdConversionHack> for ChatId {
	fn from(value: ChatIdConversionHack) -> Self {
		Self(value.0)
	}
}

impl From<ChatIdConversionHack> for i64 {
	fn from(value: ChatIdConversionHack) -> Self {
		value.0
	}
}

impl From<ChatId> for ChatIdConversionHack {
	fn from(value: ChatId) -> Self {
		Self(value.0)
	}
}