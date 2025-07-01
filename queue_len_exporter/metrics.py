from prometheus_client import Gauge


# define metric

# in normal case Gauge is useful
# name: metric name
# documentation: explain about this metric
# label: add as you need
qle_cpu_usage_percent = Gauge(
    name="qle_cpu_usage_percent",
    documentation="all cpu core average usage percent",
    labelnames=[""],
)
qle_mem_usage_percent = Gauge(
    name="qle_mem_usage_percent", documentation="mem usage percent", labelnames=[""]
)
qle_rabbitmq_queue_len = Gauge(
    name="qle_rabbitmq_queue_len",
    documentation="rabbitmq queue len",
    labelnames=["name"],
)
qle_redis_llen = Gauge(
    name="qle_redis_llen", documentation="get redis llen", labelnames=["key", "redis"]
)
qle_redis_hlen = Gauge(
    name="qle_redis_hlen",
    documentation="get redis hlen",
    labelnames=["key", "redis", "filter", "filter_alias"],
)
