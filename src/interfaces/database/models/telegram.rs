use diesel::{Associations, Identifiable, Insertable, Queryable, Selectable};
use diesel::pg::Pg;

use super::super::schema::telegram;
use super::users::RoyalnetUser;

#[derive(Debug, Clone, PartialEq, Identifiable, Queryable, Selectable, Insertable, Associations)]
#[diesel(belongs_to(RoyalnetUser, foreign_key = user_id))]
#[diesel(table_name = telegram)]
#[diesel(primary_key(telegram_id))]
#[diesel(check_for_backend(Pg))]
pub struct TelegramUser {
	pub user_id: i32,
	pub telegram_id: i64,
}
