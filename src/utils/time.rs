use chrono::{DateTime, Local};

pub fn determine_wait(target_chrono: &DateTime<Local>) -> tokio::time::Duration {
	let now_chrono = chrono::Local::now();

	let duration_chrono = target_chrono.signed_duration_since(now_chrono);
	let seconds = duration_chrono.num_seconds() + 1;

	tokio::time::Duration::from_secs(seconds as u64)
}