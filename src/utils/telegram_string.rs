use std::fmt::{Error, Write};

pub trait TelegramWrite {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), Error>
		where T: Write;

	fn to_string_telegram(&self) -> String {
		let mut result = String::new();
		self.write_telegram(&mut result).unwrap();
		result
	}
}

pub trait TelegramEscape {
	fn escape_telegram_html(self) -> String;
}

impl<T> TelegramEscape for T
where String: From<T>
{
	fn escape_telegram_html(self) -> String {
		String::from(self)
			.replace("<", "&lt;")
			.replace(">", "&gt;")
			.replace("&", "&amp;")
	}
}