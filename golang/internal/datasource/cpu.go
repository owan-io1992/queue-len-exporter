package datasource

import (
	"context"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
)

func GetCPUPercent() (float64, error) {
	percents, err := cpu.PercentWithContext(context.Background(), time.Second, false)
	if err != nil {
		return 0, err
	}
	if len(percents) > 0 {
		return percents[0], nil
	}
	return 0, nil
}
