use std::fmt::Write;

pub trait TelegramWrite {
	fn write_telegram<T>(&self, f: &mut T) -> Result<(), std::fmt::Error>
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
		let s: String = String::from(self);
		let s = s.replace("<", "&lt;");
		let s = s.replace(">", "&gt;");
		let s = s.replace("&", "&amp;");
		s
	}
}
