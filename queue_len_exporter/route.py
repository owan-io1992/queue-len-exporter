from . import metrics
from prometheus_client import generate_latest, REGISTRY
from fastapi import Request
from starlette.responses import PlainTextResponse

import logging

logger = logging.getLogger(__name__)

CONTENT_TYPE_LATEST = str("text/plain; charset=utf-8")


def register_routes(app):
    @app.get("/cpu_usage_percent")
    async def cpu_usage_percent():
        """
        Exposes CPU usage percentage as a Prometheus metric.
        This endpoint retrieves the current CPU usage and updates the 'qle_cpu_usage_percent' gauge.
        """
        from .data_source import cpu

        metric_librarie = ["qle_cpu_usage_percent"]  # use to filter output

        # get metric
        metrics.qle_cpu_usage_percent.set(cpu.cpu_percent(interval=None))

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/mem_usage_percent")
    async def mem_usage_percent():
        """
        Exposes memory usage percentage as a Prometheus metric.
        This endpoint retrieves the current memory usage and updates the 'qle_mem_usage_percent' gauge.
        """
        from .data_source import mem

        metric_librarie = ["qle_mem_usage_percent"]  # use to filter output

        # get metric
        metrics.qle_mem_usage_percent.set(mem.mem_percent())

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/rabbitmq_queue_len")
    async def rabbitmq_queue_len():
        """
        Exposes RabbitMQ queue lengths as Prometheus metrics.
        This endpoint queries the RabbitMQ management API for queue lengths
        and updates the 'qle_rabbitmq_queue_len' gauge for each queue.
        """
        from .data_source import rabbitmq
        from .config import (
            rabbitmq_host,
            rabbitmq_port,
            rabbitmq_user,
            rabbitmq_pass,
            rabbitmq_queue_pattern,
        )

        metric_librarie = ["qle_rabbitmq_queue_len"]  # use to filter output
        # cleanup old metric
        metrics.qle_rabbitmq_queue_len.clear()

        # get metric
        for k, v in rabbitmq.queue_len(
            rabbitmq_host,
            rabbitmq_port,
            rabbitmq_user,
            rabbitmq_pass,
            rabbitmq_queue_pattern,
        ).items():
            metrics.qle_rabbitmq_queue_len.labels(name=k).set(v)

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/redis_llen")
    async def redis_llen():
        """
        Exposes Redis list length (LLEN) as a Prometheus metric.
        This endpoint retrieves the length of a configured Redis list
        and updates the 'qle_redis_llen' gauge.
        """
        from .data_source import redis
        from .config import redis_url, redis_key

        metric_librarie = ["qle_redis_llen"]  # use to filter output
        # cleanup old metric
        metrics.qle_redis_llen.clear()

        # update metric
        metrics.qle_redis_llen.labels(redis=redis_url, key=redis_key).set(
            redis.list_len(redis_url, redis_key)
        )

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/scrape/redis_hlen")
    async def scrape_redis_hlen(request: Request):
        """
        Exposes Redis hash length (HLEN) as a Prometheus metric with filtering.
        This endpoint retrieves the count of elements in a Redis hash that match a specific filter.
        """
        params = request.query_params

        from .data_source import redis

        metric_librarie = ["qle_redis_hlen"]  # use to filter output
        # cleanup old metric
        metrics.qle_redis_hlen.clear()

        # update metric
        metrics.qle_redis_hlen.labels(
            redis=params["redis"],
            key=params["key"],
        ).set(redis.hlen(params["redis"], params["key"]))
        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/health")
    async def health():
        """
        Health check endpoint.
        Returns a simple "Success" message to indicate the application is running.
        """
        return PlainTextResponse("Success", media_type="text/plain")

    @app.get("/test")
    async def test(request: Request):
        """
        get all query parameter and return parameter
        """
        # parameters = request.query_params
        return request.query_params
