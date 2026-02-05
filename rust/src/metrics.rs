use prometheus::{Gauge, GaugeVec, Opts, Registry};
use lazy_static::lazy_static;

lazy_static! {
    pub static ref REGISTRY: Registry = Registry::new();

    pub static ref QLE_CPU_USAGE_PERCENT: Gauge = Gauge::new(
        "qle_cpu_usage_percent",
        "all cpu core average usage percent"
    ).unwrap();

    pub static ref QLE_MEM_USAGE_PERCENT: Gauge = Gauge::new(
        "qle_mem_usage_percent",
        "mem usage percent"
    ).unwrap();

    pub static ref QLE_RABBITMQ_QUEUE_LEN: GaugeVec = GaugeVec::new(
        Opts::new("qle_rabbitmq_queue_len", "rabbitmq queue len"),
        &["name"]
    ).unwrap();

    pub static ref QLE_REDIS_LLEN: GaugeVec = GaugeVec::new(
        Opts::new("qle_redis_llen", "get redis llen"),
        &["redis", "key"]
    ).unwrap();

    pub static ref QLE_REDIS_HLEN: GaugeVec = GaugeVec::new(
        Opts::new("qle_redis_hlen", "get redis hlen"),
        &["redis", "key"]
    ).unwrap();
}

pub fn register_metrics() {
    REGISTRY.register(Box::new(QLE_CPU_USAGE_PERCENT.clone())).unwrap();
    REGISTRY.register(Box::new(QLE_MEM_USAGE_PERCENT.clone())).unwrap();
    REGISTRY.register(Box::new(QLE_RABBITMQ_QUEUE_LEN.clone())).unwrap();
    REGISTRY.register(Box::new(QLE_REDIS_LLEN.clone())).unwrap();
    REGISTRY.register(Box::new(QLE_REDIS_HLEN.clone())).unwrap();
}
