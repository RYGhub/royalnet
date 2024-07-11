#[cfg(debug_assertions)]
pub const VERSION: &str = "DEBUG";

#[cfg(not(debug_assertions))]
pub const VERSION: &str = env!("CARGO_PKG_VERSION");
