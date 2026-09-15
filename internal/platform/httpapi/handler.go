package httpapi

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"

	"biomarker/internal/analysis"
	"biomarker/internal/platform/runtime/local"
)

// Handler exposes a local-development-only internal transport.
type Handler struct {
	runtime analysis.Runtime
}

// NewHandler creates the local HTTP handler.
func NewHandler(runtime analysis.Runtime) *Handler { return &Handler{runtime: runtime} }

// Routes returns the local development mux.
// This is not the Stage-14 public API contract.
func (h *Handler) Routes() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /healthz", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})
	mux.HandleFunc("POST /internal/runtime/execute", h.execute)
	return mux
}

func (h *Handler) execute(w http.ResponseWriter, r *http.Request) {
	r.Body = http.MaxBytesReader(w, r.Body, 1<<20)
	defer r.Body.Close()

	var req analysis.ExecutionRequest
	dec := json.NewDecoder(r.Body)
	dec.DisallowUnknownFields()
	if err := dec.Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid_request"})
		return
	}
	if err := ensureEOF(dec); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid_request"})
		return
	}

	result, err := h.runtime.Execute(r.Context(), req)
	if err != nil {
		switch {
		case errors.Is(err, analysis.ErrInvalidRequest):
			writeJSON(w, http.StatusBadRequest, result)
		case errors.Is(err, local.ErrIdempotencyConflict):
			writeJSON(w, http.StatusConflict, result)
		default:
			writeJSON(w, http.StatusInternalServerError, result)
		}
		return
	}
	writeJSON(w, http.StatusOK, result)
}

func ensureEOF(dec *json.Decoder) error {
	var extra any
	err := dec.Decode(&extra)
	if errors.Is(err, io.EOF) {
		return nil
	}
	if err == nil {
		return errors.New("multiple JSON values")
	}
	return err
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}
