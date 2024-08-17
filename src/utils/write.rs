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