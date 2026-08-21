"""Prometheus metrics definitions and exporter.

Imported for its side effects: defining the metrics and starting the HTTP
server both happen at module load. Python caches modules, so this runs once
per process even though Streamlit re-executes page scripts on every
interaction.
"""

import logging
import os
import threading

from prometheus_client import Counter, Gauge, Histogram, start_http_server

logger = logging.getLogger(__name__)

METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

# --- VQE ---

VQE_RUNS = Counter(
    "vqe_runs_total",
    "Number of VQE executions",
    ["status"],
)

VQE_DURATION = Histogram(
    "vqe_duration_seconds",
    "Wall-clock time of a VQE run",
    buckets=(0.25, 0.5, 1, 2, 5, 10, 30, 60),
)

VQE_ITERATIONS = Histogram(
    "vqe_iterations",
    "Cost function evaluations per VQE run",
    buckets=(10, 25, 50, 100, 150, 200, 250),
)

VQE_ENERGY = Gauge(
    "vqe_energy_hartree",
    "Ground state energy from the most recent VQE run",
)

# Zero is a meaningful reading for a count but not for an energy, so start
# undefined; Prometheus treats NaN as absent and draws no line until a run
# has actually produced a value.
VQE_ENERGY.set(float("nan"))

# --- RAG ---

RAG_QUERIES = Counter(
    "rag_queries_total",
    "Questions answered against the vector store",
    ["status"],
)

RAG_QUERY_DURATION = Histogram(
    "rag_query_duration_seconds",
    "Time to answer a question, including the Claude call",
    buckets=(0.5, 1, 2, 5, 10, 20, 30),
)

RAG_PAPERS_INDEXED = Counter(
    "rag_papers_indexed_total",
    "Papers added to the vector store",
)

RAG_COLLECTION_SIZE = Gauge(
    "rag_collection_size",
    "Documents currently held in the vector store",
)

_server_lock = threading.Lock()
_server_started = False


def start_metrics_server(port: int = METRICS_PORT) -> None:
    """Start the exporter once per process.

    Module caching already prevents a second call in normal operation; the
    guard covers paths that import this module differently, such as tests.
    """
    global _server_started
    with _server_lock:
        if _server_started:
            return
        try:
            start_http_server(port)
            _server_started = True
            logger.info("Metrics exporter listening on port %d", port)
        except OSError as exc:
            logger.warning("Could not start metrics exporter: %s", exc)


start_metrics_server()