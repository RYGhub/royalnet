use std::future::Future;

#[allow(unused_imports)]
use crate::services::RoyalnetService;

pub(self) mod config;

#[derive(Debug, Clone)]
pub struct RoyalnetInstance {
	#[cfg(feature = "service_telegram")]
	service_telegram: crate::services::telegram::TelegramService,

	#[cfg(not(feature = "service_telegram"))]
	service_telegram: (),

	#[cfg(feature = "service_brooch")]
	service_brooch: crate::services::brooch::BroochService,

	#[cfg(not(feature = "service_brooch"))]
	service_brooch: (),
}

impl RoyalnetInstance {
	pub async fn new() -> Self {
		Self {
			service_telegram: Self::setup_telegram_service().await,
			service_brooch: Self::setup_brooch_service().await,
		}
	}

	pub async fn run(mut self) {
		Self::run_pending_migrations();

		let future_telegram = async move {
			Self::get_telegram_future(&mut self.service_telegram).await;
		};
		let future_brooch = async move {
			Self::get_brooch_future(&mut self.service_brooch).await;
		};

		let task_telegram = tokio::spawn(future_telegram);
		let task_brooch = tokio::spawn(future_brooch);

		let _ = tokio::join!(
			task_telegram,
			task_brooch,
		);
	}

	#[cfg(feature = "interface_database")]
	fn run_pending_migrations() {
		if !config::interface_database::DATABASE_AUTOMIGRATE() {
			log::warn!("Database automigration is disabled.");
			return
		}

		log::debug!("Automatically applying database migrations...");

		log::trace!("Connecting to the database...");
		let mut db = crate::interfaces::database::connect(
			config::interface_database::DATABASE_URL()
		).expect("Unable to connect to the database to apply migrations.");

		log::trace!("Applying migrations...");
		crate::interfaces::database::migrate(&mut db)
			.expect("Failed to automatically apply migrations to the database.");

		log::trace!("Migration successful!");
	}

	#[cfg(not(feature = "interface_database"))]
	fn run_pending_migrations() {
		log::warn!("Database automigration is not compiled in.");
	}

	#[cfg(feature = "service_telegram")]
	async fn setup_telegram_service() -> crate::services::telegram::TelegramService {
		log::debug!("Setting up Telegram service...");

		crate::services::telegram::TelegramService::new(
			config::service_telegram::TELEGRAM_DATABASE_URL().clone(),
			config::service_telegram::TELEGRAM_BOT_TOKEN().clone(),
			*config::service_telegram::TELEGRAM_NOTIFICATION_CHATID(),
		).await.expect("Unable to setup Telegram service.")
	}

	#[cfg(not(feature = "service_telegram"))]
	async fn setup_telegram_service() {
		log::warn!("Telegram service is not compiled in.");
	}

	#[cfg(feature = "service_telegram")]
	fn get_telegram_future(service: &mut crate::services::telegram::TelegramService) -> impl Future<Output = ()> + '_ {
		service.run_loop()
	}

	#[cfg(not(feature = "service_telegram"))]
	#[allow(clippy::manual_async_fn)]
	fn get_telegram_future(_service: &mut ()) -> impl Future<Output = ()> + '_ {
		async {}
	}

	#[cfg(feature = "service_brooch")]
	async fn setup_brooch_service() -> crate::services::brooch::BroochService {
		log::debug!("Setting up Brooch service...");

		crate::services::brooch::BroochService::new(
			config::brooch::BROOCH_DATABASE_URL().clone(),
			config::brooch::BROOCH_GRAPHQL_URL(),
			config::brooch::BROOCH_STRATZ_TOKEN(),
			*config::brooch::BROOCH_WATCHED_GUILD_ID(),
			*config::brooch::BROOCH_MIN_PLAYERS_TO_PROCESS(),
			config::brooch::BROOCH_TELEGRAM_BOT_TOKEN().clone(),
			*config::brooch::BROOCH_NOTIFICATION_CHAT_ID(),
			*config::brooch::BROOCH_MAX_IMP_WAIT_SECS(),
		).expect("Unable to setup Brooch service.")
	}

	#[cfg(not(feature = "service_brooch"))]
	async fn setup_brooch_service() {
		log::warn!("Brooch service is not compiled in.");
	}

	#[cfg(feature = "service_brooch")]
	fn get_brooch_future(service: &mut crate::services::brooch::BroochService) -> impl Future<Output = ()> + '_ {
		service.run_loop()
	}

	#[cfg(not(feature = "service_brooch"))]
	#[allow(clippy::manual_async_fn)]
	fn get_brooch_future(_service: &mut ()) -> impl Future<Output = ()> + '_ {
		async {}
	}
}