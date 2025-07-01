# define log file path, if set None will logging to console
log_file = None
log_level = "INFO"

# mq
rabbitmq_host = "127.0.0.1"
rabbitmq_port = "15672"
rabbitmq_user = "guest"
rabbitmq_pass = "guest"
rabbitmq_queue_pattern = "^Configure.+|^Cron.+|^Monitor.+|.+listener-workers$|^notification_.+|.+NCC__FREE$|.+NSS__PAID$|^org-cloud-saving-mode-workers.+"

# runner
devconf_broker_url = "redis://127.0.0.1:5601/0"
redis_runner_queue_name = "DevConf"

# redis
redis_url = "redis://127.0.0.1:5601/0"
redis_key = "DevConf"

# mux
mux_servers = {"mux-01": "127.0.0.1"}  # name: ip
mux_redis = "redis://127.0.0.1:6379/0"
