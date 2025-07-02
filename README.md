# queue-len-exporter
this is a prometheus exporter for monitor queue length  

# support monitor source

## cpu
get CPU usage percentage as a Prometheus metric

get metrics
```bash
$ curl 127.0.0.1:8080/cpu_usage_percent
```

## memory
get memory usage percentage as a Prometheus metric

get metrics
```bash
$ curl 127.0.0.1:8080/mem_usage_percent
```

## redis
- llen
  set redis config in config.py, then use api `/redis_llen` to get metrics

config.py  
```bash
redis_url = "redis://127.0.0.1:6379/0"
redis_key = "mylist"
```

get metrics
```bash
$ curl 127.0.0.1:8080/redis_llen
# HELP qle_redis_llen get redis llen
# TYPE qle_redis_llen gauge
qle_redis_llen{key="mylist",redis="redis://127.0.0.1:6379/0"} 3.0
```

- hlen ([multi-target](https://prometheus.io/docs/guides/multi-target-exporter/) mode)
  this is [multi-target](https://prometheus.io/docs/guides/multi-target-exporter/) mode, target redis host and key will define in scrape api  
  so this don't need pre-config  

get metrics  
```bash
$ curl '127.0.0.1:8080/scrape/redis_hlen?redis=redis://127.0.0.1:6379/0&key=myhash'
# HELP qle_redis_hlen get redis hlen
# TYPE qle_redis_hlen gauge
qle_redis_hlen{key="myhash",redis="redis://127.0.0.1:6379/0"} 2.0
```

## rabbitMQ
get RabbitMQ queue lengths as Prometheus metrics.
This endpoint queries the RabbitMQ management API for queue lengths

config.py  
```bash
rabbitmq_host = "127.0.0.1"
rabbitmq_port = "15672"
rabbitmq_user = "guest"
rabbitmq_pass = "guest"
rabbitmq_queue_pattern = "^test.+"
```

get metrics
```bash
$ curl 127.0.0.1:8080/rabbitmq_queue_len
# HELP qle_rabbitmq_queue_len rabbitmq queue len
# TYPE qle_rabbitmq_queue_len gauge
qle_rabbitmq_queue_len{name="test1"} 0.0
```

# developer 
## CI test
```bash
uv run ruff format
uv run ruff check
```

## start exporter
```bash
uv run uvicorn queue_len_exporter.main:app --host 0.0.0.0 --port 8080 --reload
```

## API docs
```bash
http://127.0.0.1:8080/docs
```

# prometheus scrape config sample

```bash
scrape_configs:
  ## config for the multiple Redis targets that the exporter will scrape
  - job_name: 'redis_exporter_targets'
    static_configs:
      - targets:
        - 'redis=redis://first-redis-host:6379&key=myhash'
        - 'redis=redis://second-redis-host:6379&key=myhash'
    metrics_path: /scrape/redis_hlen
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: queue-len-exporter-exporter:8080
```
