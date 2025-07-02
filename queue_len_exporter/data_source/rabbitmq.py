import httpx
import urllib.parse
import logging

logger = logging.getLogger(__name__)


def queue_len(
    rabbitmq_host,
    rabbitmq_port,
    rabbitmq_user,
    rabbitmq_pass,
    rabbitmq_queue_pattern,
):
    ret = {}
    # https://rawcdn.githack.com/rabbitmq/rabbitmq-server/v3.12.2/deps/rabbitmq_management/priv/www/api/index.html
    safe_string = urllib.parse.quote_plus(f"{rabbitmq_queue_pattern}")
    logger.info("start get queue_len")
    queues = httpx.get(
        f"http://{rabbitmq_host}:{rabbitmq_port}/api/queues?page=1&page_size=500&name={safe_string}&use_regex=true&pagination=true",
        auth=(rabbitmq_user, rabbitmq_pass),
        timeout=10,
    ).json()
    logger.info("end get queue_len")

    for queue in queues["items"]:
        ret[queue["name"]] = queue["messages"]

    return ret
