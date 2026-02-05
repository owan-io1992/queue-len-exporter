use std::env;

pub struct Config {
    pub log_level: String,
    pub rabbitmq_host: String,
    pub rabbitmq_port: String,
    pub rabbitmq_user: String,
    pub rabbitmq_pass: String,
    pub rabbitmq_queue_pattern: String,
    pub redis_url: String,
    pub redis_key: String,
}

impl Config {
    pub fn from_env() -> Self {
        Self {
            log_level: env::var("LOG_LEVEL").unwrap_or_else(|_| "INFO".to_string()),
            rabbitmq_host: env::var("RABBITMQ_HOST").unwrap_or_else(|_| "127.0.0.1".to_string()),
            rabbitmq_port: env::var("RABBITMQ_PORT").unwrap_or_else(|_| "15672".to_string()),
            rabbitmq_user: env::var("RABBITMQ_USER").unwrap_or_else(|_| "guest".to_string()),
            rabbitmq_pass: env::var("RABBITMQ_PASS").unwrap_or_else(|_| "guest".to_string()),
            rabbitmq_queue_pattern: env::var("RABBITMQ_QUEUE_PATTERN").unwrap_or_else(|_| "^test.+".to_string()),
            redis_url: env::var("REDIS_URL").unwrap_or_else(|_| "redis://127.0.0.1:6379/0".to_string()),
            redis_key: env::var("REDIS_KEY").unwrap_or_else(|_| "mylist".to_string()),
        }
    }
}
