use anyhow::Context;
use diesel::PgConnection;
use teloxide::types::UserId;
use crate::interfaces::database::models::telegram::TelegramUser;
use crate::interfaces::database::models::users::RoyalnetUser;
use crate::utils::result::AnyResult;

impl RoyalnetUser {
	pub fn from_telegram_userid(database: &mut PgConnection, user_id: UserId) -> AnyResult<Self> {
		use diesel::prelude::*;
		use diesel::{ExpressionMethods, QueryDsl};
		use crate::interfaces::database::schema::telegram;
		use crate::interfaces::database::schema::users::dsl::*;
		use crate::interfaces::database::models::users::RoyalnetUser;

		log::trace!("Retrieving RoyalnetUser with {user_id:?}");

		Ok(
			telegram::table
				.filter(telegram::telegram_id.eq::<i64>(
					user_id.0.try_into()
						.context("Lo user_id specificato non può essere interpretato come un numero signed, il che lo rende incompatibile con il database RYG.")?
				))
				.inner_join(users)
				.select(RoyalnetUser::as_select())
				.get_result(database)
				.context("Non è stato possibile recuperare l'utente Telegram specificato dal database RYG.")?
		)
	}
}
