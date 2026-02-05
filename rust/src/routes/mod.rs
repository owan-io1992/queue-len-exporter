use axum::{
    extract::{Query, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::get,
    Router,
};
use prometheus::{Encoder, TextEncoder};
use serde::Deserialize;
use std::sync::Arc;

use crate::config::Config;
use crate::data_source::{cpu, memory, rabbitmq, redis};
use crate::metrics;

#[derive(Deserialize)]
pub struct RedisParams {
    pub redis: String,
    pub key: String,
}

pub fn create_router(config: Arc<Config>) -> Router {
    Router::new()
        .route("/cpu_usage_percent", get(cpu_usage_handler))
        .route("/mem_usage_percent", get(mem_usage_handler))
        .route("/rabbitmq_queue_len", get(rabbitmq_handler))
        .route("/redis_llen", get(redis_llen_handler))
        .route("/scrape/redis_hlen", get(redis_hlen_handler))
        .route("/health", get(health_handler))
        .route("/test", get(test_handler))
        .with_state(config)
}

async fn cpu_usage_handler() -> impl IntoResponse {
    let usage = cpu::get_cpu_usage();
    metrics::QLE_CPU_USAGE_PERCENT.set(usage as f64);
    
    render_metrics(vec!["qle_cpu_usage_percent"])
}

async fn mem_usage_handler() -> impl IntoResponse {
    let usage = memory::get_memory_usage();
    metrics::QLE_MEM_USAGE_PERCENT.set(usage as f64);
    
    render_metrics(vec!["qle_mem_usage_percent"])
}

async fn rabbitmq_handler(State(config): State<Arc<Config>>) -> impl IntoResponse {
    metrics::QLE_RABBITMQ_QUEUE_LEN.reset();
    
    match rabbitmq::get_queue_lengths(
        &config.rabbitmq_host,
        &config.rabbitmq_port,
        &config.rabbitmq_user,
        &config.rabbitmq_pass,
        &config.rabbitmq_queue_pattern,
    ).await {
        Ok(queues) => {
            for (name, len) in queues {
                metrics::QLE_RABBITMQ_QUEUE_LEN.with_label_values(&[&name]).set(len as f64);
            }
            render_metrics(vec!["qle_rabbitmq_queue_len"])
        }
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, format!("Error: {}", e)).into_response(),
    }
}

async fn redis_llen_handler(State(config): State<Arc<Config>>) -> impl IntoResponse {
    metrics::QLE_REDIS_LLEN.reset();
    
    match redis::get_list_len(&config.redis_url, &config.redis_key).await {
        Ok(len) => {
            metrics::QLE_REDIS_LLEN
                .with_label_values(&[&config.redis_url, &config.redis_key])
                .set(len as f64);
            render_metrics(vec!["qle_redis_llen"])
        }
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, format!("Error: {}", e)).into_response(),
    }
}

async fn redis_hlen_handler(Query(params): Query<RedisParams>) -> impl IntoResponse {
    metrics::QLE_REDIS_HLEN.reset();
    
    match redis::get_hash_len(&params.redis, &params.key).await {
        Ok(len) => {
            metrics::QLE_REDIS_HLEN
                .with_label_values(&[&params.redis, &params.key])
                .set(len as f64);
            render_metrics(vec!["qle_redis_hlen"])
        }
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, format!("Error: {}", e)).into_response(),
    }
}

async fn health_handler() -> &'static str {
    "Success"
}

async fn test_handler(Query(params): Query<serde_json::Value>) -> impl IntoResponse {
    axum::Json(params)
}

fn render_metrics(filter: Vec<&str>) -> Response {
    let encoder = TextEncoder::new();
    let metric_families = metrics::REGISTRY.gather();
    
    let mut buffer = Vec::new();
    // Filter metrics if needed (simulating REGISTRY.restricted_registry in Python)
    let filtered_families: Vec<_> = metric_families
        .into_iter()
        .filter(|mf| filter.contains(&mf.get_name()))
        .collect();
        
    encoder.encode(&filtered_families, &mut buffer).unwrap();
    
    Response::builder()
        .header("Content-Type", "text/plain; charset=utf-8")
        .body(axum::body::Body::from(buffer))
        .unwrap()
}
