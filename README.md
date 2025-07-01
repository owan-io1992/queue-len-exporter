# queue-len-exporter
this is a prometheus exporter for monitor queue length  

# support monitor source
## redis

## rabbitMQ

# start eporter

```bash
uv run uvicorn queue_len_exporter.main:app --host 0.0.0.0 --port 8080 --reload
```

# prometheus scrape config sample

```bash
scrape_configs:
  ## config for the multiple Redis targets that the exporter will scrape
  - job_name: 'redis_exporter_targets'
    static_configs:
      - targets:
        - 'key=asd,redis=redis://first-redis-host:6379'
        - redis://second-redis-host:6379
        - redis://second-redis-host:6380
        - redis://second-redis-host:6381
    metrics_path: /scrape/rediskey_llen
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: queue-len-exporter-exporter:50000
```