use std::str::FromStr;

use crate::interfaces::database::models::MatchmakingId;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MatchmakingTelegramKeyboardCallback {
	Yes,
	Plus5Min,
	Plus15Min,
	Plus60Min,
	Maybe,
	DontWait,
	Cant,
	Wont,
}

impl MatchmakingTelegramKeyboardCallback {
	/// Create callback data representing the [MatchmakingTelegramKeyboardCallback] in the given [MatchmakingId].
	pub fn callback_data(self, matchmaking_id: MatchmakingId) -> String {
		matchmaking_id.callback_data(self.into())
	}
	
	pub fn inline_button(self, matchmaking_id: MatchmakingId, text: &str) -> teloxide::types::InlineKeyboardButton {
		teloxide::types::InlineKeyboardButton::new(
			text,
			teloxide::types::InlineKeyboardButtonKind::CallbackData(
				self.callback_data(matchmaking_id)
			),
		)
	}
}

impl FromStr for MatchmakingTelegramKeyboardCallback {
	type Err = anyhow::Error;
	
	fn from_str(s: &str) -> Result<Self, Self::Err> {
		Ok(
			match s {
				"yes" => Self::Yes,
				"5min" => Self::Plus5Min,
				"15min" => Self::Plus15Min,
				"60min" => Self::Plus60Min,
				"maybe" => Self::Maybe,
				"dontw" => Self::DontWait,
				"cant" => Self::Cant,
				"wont" => Self::Wont,
				x => anyhow::bail!("Unknown keyboard callback: {x:?}"),
			}
		)
	}
}

impl From<MatchmakingTelegramKeyboardCallback> for &'static str {
	fn from(value: MatchmakingTelegramKeyboardCallback) -> Self {
		match value {
			MatchmakingTelegramKeyboardCallback::Yes => "yes",
			MatchmakingTelegramKeyboardCallback::Plus5Min => "5min",
			MatchmakingTelegramKeyboardCallback::Plus15Min => "15min",
			MatchmakingTelegramKeyboardCallback::Plus60Min => "60min",
			MatchmakingTelegramKeyboardCallback::Maybe => "maybe",
			MatchmakingTelegramKeyboardCallback::DontWait => "dontw",
			MatchmakingTelegramKeyboardCallback::Cant => "cant",
			MatchmakingTelegramKeyboardCallback::Wont => "wont",
		}
	}
}