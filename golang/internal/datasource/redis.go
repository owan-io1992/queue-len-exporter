package datasource

import (
	"context"
	"fmt"
	"net/url"
	"strconv"
	"strings"

	"github.com/redis/go-redis/v9"
)

func getRedisClient(redisURL string) (redis.UniversalClient, error) {
	u, err := url.Parse(redisURL)
	if err != nil {
		return nil, err
	}

	if u.Scheme == "redis" {
		opts, err := redis.ParseURL(redisURL)
		if err != nil {
			return nil, err
		}
		return redis.NewClient(opts), nil
	} else if u.Scheme == "sentinel" {
		addrs := strings.Split(u.Host, ",")
		query := u.Query()
		serviceName := query.Get("service_name")
		if serviceName == "" {
			serviceName = "default"
		}
		dbStr := strings.Trim(u.Path, "/")
		db := 0
		if dbStr != "" {
			db, _ = strconv.Atoi(dbStr)
		}

		return redis.NewFailoverClient(&redis.FailoverOptions{
			MasterName:    serviceName,
			SentinelAddrs: addrs,
			DB:            db,
		}), nil
	}

	return nil, fmt.Errorf("invalid redis URL scheme: %s", u.Scheme)
}

func GetRedisLLen(redisURL, key string) (int64, error) {
	client, err := getRedisClient(redisURL)
	if err != nil {
		return 0, err
	}
	defer client.Close()

	ctx := context.Background()
	return client.LLen(ctx, key).Result()
}

func GetRedisHLen(redisURL, key string) (int64, error) {
	client, err := getRedisClient(redisURL)
	if err != nil {
		return 0, err
	}
	defer client.Close()

	ctx := context.Background()
	return client.HLen(ctx, key).Result()
}
