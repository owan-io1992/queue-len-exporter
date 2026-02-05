use std::sync::Arc;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

mod config;
mod data_source;
mod metrics;
mod routes;

#[tokio::main]
async fn main() {
    // Banner
    println!("{}", r#"
  __ _ _   _  ___ _   _  ___     | | ___ _ __     _____  _ __   ___  _ __| |_ ___ _ __ 
 / _` | | | |/ _ \ | | |/ _ \____| |/ _ \ '_ \   / _ \ \/ / '_ \ / _ \| '__| __/ _ \ '__|
| (_| | |_| |  __/ |_| |  __/____| |  __/ | | | |  __/>  <| |_) | (_) | |  | ||  __/ |   
 \__, |\__,_|\___|\__,_|\___|    |_|\___|_| |_|  \___/_/\_\ .__/ \___/|_|   \__\___|_|   
    |_|                                                   |_|                            
"#);

    // Initialize config
    let config = Arc::new(config::Config::from_env());

    // Initialize tracing
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(tracing_subscriber::EnvFilter::new(&config.log_level))
        .init();

    // Register metrics
    metrics::register_metrics();

    // Create app
    let app = routes::create_router(config.clone());

    // Start server
    let addr = std::net::SocketAddr::from(([0, 0, 0, 0], 8000));
    tracing::info!("listening on {}", addr);
    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}
