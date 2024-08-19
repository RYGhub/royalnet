use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use crate::newtype_sql;

use super::super::schema::telegram;
use super::users::{RoyalnetUser, RoyalnetUserId};

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = telegram)]
#[diesel(primary_key(telegram_id))]
#[diesel(check_for_backend(Pg))]
pub struct TelegramUser {
	pub user_id: RoyalnetUserId,
	pub telegram_id: TelegramUserId,
}

newtype_sql!(pub TelegramUserId: diesel::sql_types::Int8 as i64);
newtype_sql!(pub TelegramChatId: diesel::sql_types::Int8 as i64);
newtype_sql!(pub TelegramMessageId: diesel::sql_types::Int4 as i32);

#[cfg(feature = "service_telegram")]
mod telegram_ext {
	use super::*;

	impl From<teloxide::types::ChatId> for TelegramChatId {
		fn from(value: teloxide::types::ChatId) -> Self {
			Self(value.0)
		}
	}
	
	impl From<TelegramChatId> for teloxide::types::ChatId {
		fn from(value: TelegramChatId) -> Self {
			Self(value.0)
		}
	}
	
	impl From<teloxide::types::UserId> for TelegramUserId {
		fn from(value: teloxide::types::UserId) -> Self {
			// FIXME: this surely seems like a great idea
			Self(value.0 as i64)
		}
	}
	
	impl From<TelegramUserId> for teloxide::types::UserId {
		fn from(value: TelegramUserId) -> Self {
			// FIXME: this surely seems like a great idea
			Self(value.0 as u64)
		}
	}
	
	impl From<teloxide::types::MessageId> for TelegramMessageId {
		fn from(value: teloxide::types::MessageId) -> Self {
			Self(value.0)
		}
	}
	
	impl From<TelegramMessageId> for teloxide::types::MessageId {
		fn from(value: TelegramMessageId) -> Self {
			Self(value.0)
		}
	}
}