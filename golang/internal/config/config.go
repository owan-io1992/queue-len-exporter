package config

import (
	"os"
)

type Config struct {
	LogFile               string
	LogLevel              string
	RabbitMQHost          string
	RabbitMQPort          string
	RabbitMQUser          string
	RabbitMQPass          string
	RabbitMQQueuePattern string
	RedisURL              string
	RedisKey              string
}

func LoadConfig() *Config {
	return &Config{
		LogFile:               getEnv("LOG_FILE", ""),
		LogLevel:              getEnv("LOG_LEVEL", "INFO"),
		RabbitMQHost:          getEnv("RABBITMQ_HOST", "127.0.0.1"),
		RabbitMQPort:          getEnv("RABBITMQ_PORT", "15672"),
		RabbitMQUser:          getEnv("RABBITMQ_USER", "guest"),
		RabbitMQPass:          getEnv("RABBITMQ_PASS", "guest"),
		RabbitMQQueuePattern: getEnv("RABBITMQ_QUEUE_PATTERN", "^test.+"),
		RedisURL:              getEnv("REDIS_URL", "redis://127.0.0.1:6379/0"),
		RedisKey:              getEnv("REDIS_KEY", "mylist"),
	}
}

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}
