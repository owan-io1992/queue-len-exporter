package datasource

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"time"
)

type RabbitMQResponse struct {
	Items []struct {
		Name     string `json:"name"`
		Messages int    `json:"messages"`
	} `json:"items"`
}

func GetRabbitMQQueueLen(host, port, user, pass, pattern string) (map[string]int, error) {
	safePattern := url.QueryEscape(pattern)
	apiURL := fmt.Sprintf("http://%s:%s/api/queues?page=1&page_size=500&name=%s&use_regex=true&pagination=true", host, port, safePattern)

	client := &http.Client{
		Timeout: 10 * time.Second,
	}

	req, err := http.NewRequest("GET", apiURL, nil)
	if err != nil {
		return nil, err
	}
	req.SetBasicAuth(user, pass)

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("unexpected status code: %d", resp.StatusCode)
	}

	var rabbitResp RabbitMQResponse
	if err := json.NewDecoder(resp.Body).Decode(&rabbitResp); err != nil {
		return nil, err
	}

	result := make(map[string]int)
	for _, item := range rabbitResp.Items {
		result[item.Name] = item.Messages
	}

	return result, nil
}
