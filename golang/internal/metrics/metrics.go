package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
)

var (
	Registry = prometheus.NewRegistry()

	QleCPUUsagePercent = prometheus.NewGauge(prometheus.GaugeOpts{
		Name: "qle_cpu_usage_percent",
		Help: "all cpu core average usage percent",
	})
	QleMemUsagePercent = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "qle_mem_usage_percent",
		Help: "mem usage percent",
	})
	QleRabbitMQQueueLen = promauto.NewGaugeVec(prometheus.GaugeOpts{
		Name: "qle_rabbitmq_queue_len",
		Help: "rabbitmq queue len",
	}, []string{"name"})
	QleRedisLLen = promauto.NewGaugeVec(prometheus.GaugeOpts{
		Name: "qle_redis_llen",
		Help: "get redis llen",
	}, []string{"key", "redis"})
	QleRedisHLen = prometheus.NewGaugeVec(prometheus.GaugeOpts{
		Name: "qle_redis_hlen",
		Help: "get redis hlen",
	}, []string{"redis", "key"})
)

func init() {
	Registry.MustRegister(QleCPUUsagePercent)
	Registry.MustRegister(QleMemUsagePercent)
	Registry.MustRegister(QleRabbitMQQueueLen)
	Registry.MustRegister(QleRedisLLen)
	Registry.MustRegister(QleRedisHLen)
}
