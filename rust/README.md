# Queue Len Exporter (Rust Refactor)

This is a Rust refactor of the `queue-len-exporter` project, originally written in Python.

## Features
- Prometheus metrics for:
  - CPU usage percentage
  - Memory usage percentage
  - RabbitMQ queue lengths (with regex support)
  - Redis list length (LLEN)
  - Redis hash length (HLEN)
- REST API using Axum
- Configuration via environment variables

## Endpoints
- `GET /cpu_usage_percent`
- `GET /mem_usage_percent`
- `GET /rabbitmq_queue_len`
- `GET /redis_llen`
- `GET /scrape/redis_hlen?redis=<url>&key=<key>`
- `GET /health`
- `GET /test`

## Configuration
The following environment variables can be used for configuration:
- `LOG_LEVEL`: Log level (default: `INFO`)
- `RABBITMQ_HOST`: RabbitMQ host (default: `127.0.0.1`)
- `RABBITMQ_PORT`: RabbitMQ management port (default: `15672`)
- `RABBITMQ_USER`: RabbitMQ user (default: `guest`)
- `RABBITMQ_PASS`: RabbitMQ password (default: `guest`)
- `RABBITMQ_QUEUE_PATTERN`: Regex pattern for queues (default: `^test.+`)
- `REDIS_URL`: Redis connection URL (default: `redis://127.0.0.1:6379/0`)
- `REDIS_KEY`: Default Redis key for LLEN (default: `mylist`)

## How to Run
Ensure you have Rust installed (managed by `mise` in this project).

```bash
cd rust
cargo run
```

## Build
To build for production:
```bash
cd rust
cargo build --release
```
