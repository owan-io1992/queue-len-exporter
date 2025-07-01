import redis
from redis.sentinel import Sentinel
from urllib.parse import parse_qs, urlparse
import logging
logger = logging.getLogger(__name__)


def get_redis_connection(redis_url):
    parsed_url = urlparse(redis_url)
    query_params = parse_qs(parsed_url.query)
    params_dict = {key: value[0] for key, value in query_params.items()}

    if parsed_url.scheme == 'redis':
        # Single instance Redis
        return redis.Redis.from_url(redis_url, max_connections=1)
    elif parsed_url.scheme == 'sentinel':
        # Sentinel
        sentinel_hosts = parsed_url.netloc.split(',')
        sentinel_hosts = [host.split(':') for host in sentinel_hosts]
        sentinel_hosts = [(host[0], int(host[1])) for host in sentinel_hosts]

        service_name = str(params_dict.get('service_name', "default"))

        db = parsed_url.path.strip('/')
        max_connections = int(params_dict.get('max_connections', 1))
        socket_connect_timeout = int(
            params_dict.get('socket_connect_timeout', 1))
        socket_timeout = int(params_dict.get('socket_timeout', 1))

        logger.debug(
            f"sentinel_hosts: {sentinel_hosts}, service_name: {service_name}, db: {db}, max_connections: {max_connections}, socket_connect_timeout: {socket_connect_timeout}, socket_timeout: {socket_timeout}")

        sentinel = Sentinel(sentinel_hosts, socket_timeout=socket_timeout,
                            socket_connect_timeout=socket_connect_timeout)
        return sentinel.slave_for(db=db, service_name=service_name, max_connections=1)
    else:
        raise ValueError("Invalid Redis URL scheme")


def keys_count(redis_url, key_patten):
    with get_redis_connection(redis_url) as r:
        while max_loop > 0:
            # Perform the scan
            cursor, partial_keys = r.scan(cursor, match=key_patten)
            # caculate length
            queue_length += (len(partial_keys))

            max_loop -= 1
            # Check if the cursor is 0, indicating the end of the scan
            if cursor == 0:
                break
    return queue_length


def list_len(redis_url, key_name):
    queue_length = 0
    with get_redis_connection(redis_url) as r:
        logger.info(f"start list_len: {key_name}")
        queue_length = r.llen(key_name)
        logger.info(f"end list_len: {key_name}")
    return queue_length


hash_data = {}


def hlen(redis_url, key_name, filter, no_cache):
    global hash_data
    redis_length = 0
    if no_cache == "true":
        logger.info("hlen: config no_cache, pull key")
        with get_redis_connection(redis_url) as r:
            hash_data[f"{redis_url}_{key_name}"] = r.hgetall(key_name)

    for k, v in hash_data[f"{redis_url}_{key_name}"].items():
        if v.decode() == filter:
            redis_length += 1

    logger.info(f"hlen: redis_url={redis_url}, filter={filter}, redis_length={redis_length}")

    return redis_length
