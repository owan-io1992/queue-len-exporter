package datasource

import (
	"context"
	"math"

	"github.com/shirou/gopsutil/v3/mem"
)

func GetMemPercent() (float64, error) {
	v, err := mem.VirtualMemoryWithContext(context.Background())
	if err != nil {
		return 0, err
	}
	percent := float64(v.Used) / float64(v.Total)
	return math.Round(percent*10000) / 10000, nil
}
