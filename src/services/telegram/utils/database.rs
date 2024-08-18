use anyhow::Context;
use diesel::PgConnection;
use teloxide::types::UserId;
use crate::interfaces::database::models::RoyalnetUser;
use crate::utils::anyhow_result::AnyResult;

impl RoyalnetUser {
	pub fn from_telegram_userid(database: &mut PgConnection, user_id: UserId) -> AnyResult<Self> {
		use crate::interfaces::database::query_prelude::*;
		use schema::{telegram, users};

		log::trace!("Retrieving RoyalnetUser with {user_id:?}");

		telegram::table
			.filter(telegram::telegram_id.eq::<i64>(
				user_id.0.try_into()
					.context("Lo user_id specificato non può essere interpretato come un numero signed, il che lo rende incompatibile con il database RYG.")?
			))
			.inner_join(users::table)
			.select(RoyalnetUser::as_select())
			.get_result(database)
			.context("Non è stato possibile recuperare l'utente Telegram specificato dal database RYG.")
	}
}
