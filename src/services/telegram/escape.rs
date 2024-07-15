pub trait EscapableInTelegramHTML {
	fn escape_telegram_html(self) -> String;
}

impl<T> EscapableInTelegramHTML for T
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