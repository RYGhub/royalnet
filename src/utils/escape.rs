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