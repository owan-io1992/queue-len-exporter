package main

import (
	"fmt"
	"log"
	"os"

	"github.com/owan-io1992/queue-len-exporter/internal/config"
	"github.com/owan-io1992/queue-len-exporter/internal/server"
)

func main() {
	fmt.Println(`
                                      _                                                  _             
  __ _ _   _  ___ _   _  ___         | | ___ _ __         _____  ___ __   ___  _ __ _ __| |_ ___ _ __ 
 / _  | | | |/ _ \ | | |/ _ \ _____  | |/ _ \ '_ \ _____ / _ \ \/ / '_ \ / _ \| '__| '__| __/ _ \ '__|
| (_| | |_| |  __/ |_| |  __/|_____| | |  __/ | | |_____|  __/>  <| |_) | (_) | |  | |  | |_  __/ |   
 \__, |\__,_|\___|\__,_|\___|        |_|\___|_| |_|      \___/_/\_\ .__/ \___/|_|  |_|   \__\___|_|   
    |_|                                                           |_|                                 
`)

	cfg := config.LoadConfig()

	if cfg.LogFile != "" {
		f, err := os.OpenFile(cfg.LogFile, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
		if err != nil {
			log.Fatalf("error opening file: %v", err)
		}
		defer f.Close()
		log.SetOutput(f)
	}
	// For simplicity, we just use standard log. In a production app,
	// you'd use a more sophisticated logger like zap or zerolog
	// and set the log level.

	s := server.NewServer(cfg)
	addr := ":8000" // Default port as in many FastAPI apps
	fmt.Printf("Starting server at %s\n", addr)
	if err := s.Run(addr); err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
