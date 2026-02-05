# Agent Guide: queue-len-exporter

This project is a Prometheus exporter designed to monitor various metrics, including CPU usage, memory usage, and queue lengths from Redis and RabbitMQ. It is built using FastAPI and follows a modular design for easy extension to new data sources.

## System Overview

The application is structured as follows:

- **Entry Point**: `queue_len_exporter/main.py` initializes the FastAPI application and logs.
- **Routing**: `queue_len_exporter/route.py` defines the HTTP endpoints. Each endpoint typically:
    1. Imports the relevant data source collector.
    2. Clears/updates the corresponding Prometheus metric.
    3. Returns the metric in Prometheus format using `REGISTRY.restricted_registry`.
- **Metrics Definition**: `queue_len_exporter/metrics.py` contains all the Prometheus `Gauge` objects used in the project.
- **Data Sources**: `queue_len_exporter/data_source/` contains the logic for interacting with external systems (Redis, RabbitMQ, psutil) to fetch raw data.
- **Configuration**: `queue_len_exporter/config.py` holds settings for RabbitMQ connections, Redis URLs, and logging.

## Key Components

### Core Modules
- `queue_len_exporter/main.py`: App initialization and registry cleanup.
- `queue_len_exporter/route.py`: Endpoint definitions (`/cpu_usage_percent`, `/redis_llen`, etc.).
- `queue_len_exporter/metrics.py`: Metric declarations.

### Data Sources
- `cpu.py`: Uses `psutil` for CPU metrics.
- `mem.py`: Uses `psutil` for memory metrics.
- `redis.py`: Uses `redis-py` for `LLEN` and `HLEN`.
- `rabbitmq.py`: Uses `httpx` to query the RabbitMQ Management API.

## Development Workflow

### Requirements
- Python 3.13.5
- [uv](https://github.com/astral-sh/uv) for dependency management.

### Common Commands
- **Run the exporter**: `uv run uvicorn queue_len_exporter.main:app --reload`
- **Format code**: `uv run ruff format`
- **Lint code**: `uv run ruff check`

## Extension Guide

To add a new metric source:
1. Create a new collector in `queue_len_exporter/data_source/`.
2. Define a new metric in `queue_len_exporter/metrics.py`.
3. Add a new endpoint in `queue_len_exporter/route.py` to trigger the collection and expose the metric.
4. (Optional) Add configuration parameters in `queue_len_exporter/config.py`.

## Project Conventions
- Metrics should be prefixed with `qle_`.
- Use `REGISTRY.restricted_registry` in routes to ensure only relevant metrics are returned for a specific endpoint.
- Prefer `uv` for all tool executions.
