# Project Analysis: queue-len-exporter

This document provides an analysis of the `queue-len-exporter` Python project, detailing its purpose and functionality. This project is a Prometheus exporter designed to collect and expose various system and application-specific metrics. It leverages FastAPI to create HTTP endpoints that, when scraped by Prometheus, provide real-time data.

## Core Functionality

*   **FastAPI Web Server**: The project runs a web server using FastAPI, exposing several HTTP endpoints for metric collection.
*   **Prometheus Integration**: It defines custom Prometheus Gauge metrics for different data points and exposes them in a format that Prometheus can scrape. It also unregisters some default Prometheus metrics (GC_COLLECTOR, PLATFORM_COLLECTOR, PROCESS_COLLECTOR) to ensure a clean output.
*   **Configurable Data Sources**: The exporter is designed to pull metrics from various sources, with configurable parameters managed through `config.py`.
    *   **RabbitMQ Queue Lengths**: It connects to a RabbitMQ management API to fetch the lengths of queues. The queues to monitor are identified by a configurable regular expression pattern (`rabbitmq_queue_pattern`). This is crucial for monitoring message queue backlogs.
    *   **Redis List and Hash Lengths**: It connects to Redis instances (supporting both single instance Redis and Redis Sentinel setups) to retrieve the length of Redis lists (`llen`) and the count of elements in Redis hashes (`hlen`). This allows for monitoring of data structures used as queues or other key-value stores in Redis.
    *   **CPU and Memory Usage**: It collects basic system metrics such as CPU usage percentage and memory usage percentage using the `psutil` library.
*   **Dynamic Configuration**: All critical connection details and patterns for RabbitMQ and Redis, along with logging levels, are externalized in the `config.py` file. This design promotes easy configuration and adaptation to different environments without code changes.
*   **Logging**: The project includes basic logging functionality, allowing output to be directed to either the console or a specified log file, configurable via `log_file` and `log_level` in `config.py`.

## Project Structure Overview

*   [`queue_len_exporter/main.py`](queue_len_exporter/main.py): The primary entry point of the application. It initializes the FastAPI server, sets up logging, unregisters default Prometheus metrics, and registers the API routes.
*   [`queue_len_exporter/config.py`](queue_len_exporter/config.py): Contains all configurable parameters for the exporter, including RabbitMQ and Redis connection details, queue patterns, and logging settings.
*   [`queue_len_exporter/metrics.py`](queue_len_exporter/metrics.py): Defines the Prometheus Gauge metrics that the exporter will expose. Each metric is given a name and a documentation string, and some include labels for additional context.
*   [`queue_len_exporter/route.py`](queue_len_exporter/route.py): Defines the FastAPI endpoints. Each endpoint is responsible for calling the appropriate data source function, updating the corresponding Prometheus metric, and returning the metrics in Prometheus exposition format.
*   [`queue_len_exporter/data_source/`](queue_len_exporter/data_source/): This directory contains modules responsible for fetching data from specific sources:
    *   [`queue_len_exporter/data_source/cpu.py`](queue_len_exporter/data_source/cpu.py): Implements the logic to get CPU usage.
    *   [`queue_len_exporter/data_source/mem.py`](queue_len_exporter/data_source/mem.py): Implements the logic to get memory usage.
    *   [`queue_len_exporter/data_source/rabbitmq.py`](queue_len_exporter/data_source/rabbitmq.py): Implements the logic to query RabbitMQ for queue lengths.
    *   [`queue_len_exporter/data_source/redis.py`](queue_len_exporter/data_source/redis.py): Implements the logic to connect to Redis and retrieve list (`llen`) and hash (`hlen`) lengths.

In essence, `queue_len_exporter` serves as a robust and configurable tool for exposing critical queue and system performance metrics to a Prometheus monitoring system.