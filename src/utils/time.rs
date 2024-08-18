pub fn chrono_to_tokio_duration(duration: chrono::TimeDelta) -> Option<tokio::time::Duration> {
	let nanos = duration.num_nanoseconds()?;

	Some(
		tokio::time::Duration::from_nanos(nanos as u64)
	)
}

pub async fn sleep_chrono(until: &chrono::DateTime<chrono::Local>) {
	let now = chrono::Local::now();

	let duration = until.signed_duration_since(now);

	let duration = chrono_to_tokio_duration(duration)
		.expect("Nanoseconds to not overflow u64");

	tokio::time::sleep(duration).await;
}
