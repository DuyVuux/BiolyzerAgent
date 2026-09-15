package main

import (
	"context"
	"errors"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"biomarker/internal/platform/httpapi"
	"biomarker/internal/platform/model"
	einoruntime "biomarker/internal/platform/runtime/eino"
	"biomarker/internal/platform/runtime/local"
	"biomarker/internal/safety"
)

func main() {
	ctx := context.Background()

	generator := model.NewDeterministicGenerator()
	gate := safety.NewEvaluator()
	workflow, err := einoruntime.NewWorkflow(ctx, generator, gate)
	if err != nil {
		log.Fatalf("compile runtime workflow: %v", err)
	}

	runtime := local.NewRuntime(workflow, local.NewLedger())
	handler := httpapi.NewHandler(runtime)

	addr := os.Getenv("BIOMARKER_ADDR")
	if addr == "" {
		addr = "127.0.0.1:8080"
	}

	server := &http.Server{
		Addr:              addr,
		Handler:           handler.Routes(),
		ReadHeaderTimeout: 5 * time.Second,
		ReadTimeout:       10 * time.Second,
		WriteTimeout:      15 * time.Second,
		IdleTimeout:       30 * time.Second,
	}

	errCh := make(chan error, 1)
	go func() {
		log.Printf("stage-09 local runtime listening on %s", addr)
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			errCh <- err
		}
	}()

	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)

	select {
	case sig := <-stop:
		log.Printf("shutdown signal=%s", sig)
	case err := <-errCh:
		log.Fatalf("server error: %v", err)
	}

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Printf("graceful shutdown error: %v", err)
	}
}
