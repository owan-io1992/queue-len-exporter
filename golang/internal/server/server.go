package server

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/owan-io1992/queue-len-exporter/internal/config"
	"github.com/owan-io1992/queue-len-exporter/internal/datasource"
	"github.com/owan-io1992/queue-len-exporter/internal/metrics"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	dto "github.com/prometheus/client_model/go"
	"github.com/prometheus/common/expfmt"
)

type Server struct {
	cfg    *config.Config
	engine *gin.Engine
}

func NewServer(cfg *config.Config) *Server {
	engine := gin.Default()
	s := &Server{
		cfg:    cfg,
		engine: engine,
	}
	s.registerRoutes()
	return s
}

func (s *Server) registerRoutes() {
	s.engine.GET("/cpu_usage_percent", s.cpuUsagePercent)
	s.engine.GET("/mem_usage_percent", s.memUsagePercent)
	s.engine.GET("/rabbitmq_queue_len", s.rabbitmqQueueLen)
	s.engine.GET("/redis_llen", s.redisLLen)
	s.engine.GET("/scrape/redis_hlen", s.redisHLen)
	s.engine.GET("/health", func(c *gin.Context) {
		c.String(http.StatusOK, "Success")
	})
	s.engine.GET("/test", func(c *gin.Context) {
		c.JSON(http.StatusOK, c.Request.URL.Query())
	})
	// Legacy metrics endpoint if needed
	s.engine.GET("/metrics", gin.WrapH(promhttp.HandlerFor(metrics.Registry, promhttp.HandlerOpts{})))
}

func (s *Server) cpuUsagePercent(c *gin.Context) {
	val, err := datasource.GetCPUPercent()
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}
	metrics.QleCPUUsagePercent.Set(val)
	s.renderMetrics(c, "qle_cpu_usage_percent")
}

func (s *Server) memUsagePercent(c *gin.Context) {
	val, err := datasource.GetMemPercent()
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}
	metrics.QleMemUsagePercent.Set(val)
	s.renderMetrics(c, "qle_mem_usage_percent")
}

func (s *Server) rabbitmqQueueLen(c *gin.Context) {
	res, err := datasource.GetRabbitMQQueueLen(
		s.cfg.RabbitMQHost,
		s.cfg.RabbitMQPort,
		s.cfg.RabbitMQUser,
		s.cfg.RabbitMQPass,
		s.cfg.RabbitMQQueuePattern,
	)
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}

	metrics.QleRabbitMQQueueLen.Reset()
	for k, v := range res {
		metrics.QleRabbitMQQueueLen.WithLabelValues(k).Set(float64(v))
	}
	s.renderMetrics(c, "qle_rabbitmq_queue_len")
}

func (s *Server) redisLLen(c *gin.Context) {
	val, err := datasource.GetRedisLLen(s.cfg.RedisURL, s.cfg.RedisKey)
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}
	metrics.QleRedisLLen.Reset()
	metrics.QleRedisLLen.WithLabelValues(s.cfg.RedisKey, s.cfg.RedisURL).Set(float64(val))
	s.renderMetrics(c, "qle_redis_llen")
}

func (s *Server) redisHLen(c *gin.Context) {
	redisURL := c.Query("redis")
	key := c.Query("key")
	if redisURL == "" || key == "" {
		c.String(http.StatusBadRequest, "missing redis or key parameter")
		return
	}

	val, err := datasource.GetRedisHLen(redisURL, key)
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}
	metrics.QleRedisHLen.Reset()
	metrics.QleRedisHLen.WithLabelValues(redisURL, key).Set(float64(val))
	s.renderMetrics(c, "qle_redis_hlen")
}

func (s *Server) renderMetrics(c *gin.Context, names ...string) {
	mfs, err := metrics.Registry.Gather()
	if err != nil {
		c.String(http.StatusInternalServerError, err.Error())
		return
	}
	
	// Filter metrics by name
	var filteredMFS []*dto.MetricFamily
	for _, mf := range mfs {
		for _, name := range names {
			if mf.GetName() == name {
				filteredMFS = append(filteredMFS, mf)
				break
			}
		}
	}
	
	c.Header("Content-Type", "text/plain; charset=utf-8")
	enc := expfmt.NewEncoder(c.Writer, expfmt.FmtText)
	for _, mf := range filteredMFS {
		enc.Encode(mf)
	}
}

func (s *Server) Run(addr string) error {
	return s.engine.Run(addr)
}
