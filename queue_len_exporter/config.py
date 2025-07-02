# define log file path, if set None will logging to console
log_file = None
log_level = "INFO"

# use for /rabbitmq_queue_len
rabbitmq_host = "127.0.0.1"
rabbitmq_port = "15672"
rabbitmq_user = "guest"
rabbitmq_pass = "guest"
rabbitmq_queue_pattern = "^test.+"

# use for /redis_llen
# schema support redis/sentinel
redis_url = "redis://127.0.0.1:6379/0"
redis_key = "mylist"

# use for /scrape/redis_hlen
mux_servers = {"mux-01": "127.0.0.1"}  # name: ip
mux_redis = "redis://127.0.0.1:6379/0"
