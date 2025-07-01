from . import metrics
from prometheus_client import generate_latest, REGISTRY
from fastapi import Request
from starlette.responses import PlainTextResponse

import logging

logger = logging.getLogger(__name__)

CONTENT_TYPE_LATEST = str("text/plain; charset=utf-8")


def register_routes(app):
    def parameter_parser(request: Request):
        parameters = request.query_params.get("target").split(",")
        config = dict(s.split("=") for s in parameters)
        logger.info(f"endpoint: scrape/rediskey_hlen, config={config}")
        return config

    @app.get("/cpu_usage_percent")
    async def cpu_usage_percent():
        from .data_source import cpu

        metric_librarie = ["qle_cpu_usage_percent"]  # use to filter output
        # cleanup old metric
        metrics.qle_cpu_usage_percent.clear()

        # get metric
        metrics.qle_cpu_usage_percent.labels().set(cpu.cpu_percent(interval=None))

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/mem_usage_percent")
    async def mem_usage_percent():
        from .data_source import mem

        metric_librarie = ["qle_mem_usage_percent"]  # use to filter output
        # cleanup old metric
        metrics.qle_mem_usage_percent.clear()

        # get metric
        metrics.qle_mem_usage_percent.labels().set(mem.mem_percent())

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/rabbitmq_queue_len")
    async def rabbitmq_queue_len():
        from .data_source import rabbitmq

        metric_librarie = ["qle_rabbitmq_queue_len"]  # use to filter output
        # cleanup old metric
        metrics.qle_rabbitmq_queue_len.clear()

        # get metric
        for k, v in rabbitmq.queue_len().items():
            metrics.qle_rabbitmq_queue_len.labels(name=k).set(v)

        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/redis_llen")
    async def redis_llen():
        from .data_source import redis
        from config import redis_url, redis_key

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
        config = parameter_parser(request)

        from .data_source import redis

        metric_librarie = ["qle_redis_hlen"]  # use to filter output
        # cleanup old metric
        metrics.qle_redis_hlen.clear()

        # update metric
        metrics.qle_redis_hlen.labels(
            redis=config["redis"],
            key=config["key"],
            filter=config["filter"],
            filter_alias=config["filter_alias"],
        ).set(
            redis.hlen(
                config["redis"], config["key"], config["filter"], config["no_cache"]
            )
        )
        return PlainTextResponse(
            generate_latest(REGISTRY.restricted_registry(metric_librarie)),
            media_type=CONTENT_TYPE_LATEST,
        )

    @app.get("/health")
    async def root():
        return PlainTextResponse("Success", media_type="text/plain")
