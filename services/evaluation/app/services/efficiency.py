"""
efficiency.py
Computational efficiency metrics computation.

Computes latency percentiles, throughput, and resource usage from
inference timing data attached to prediction entries.
"""

import logging
import statistics
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def compute_latency_stats(latencies_ms: List[float]) -> Dict[str, float]:
    """
    Computes latency statistics from a list of per-image inference times.

    Args:
        latencies_ms: List of inference latencies in milliseconds.

    Returns:
        Dict with avg, p50, p95, p99, max latency values.
    """
    if not latencies_ms:
        return {
            "avg_latency_ms": 0.0,
            "p50_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "p99_latency_ms": 0.0,
            "max_latency_ms": 0.0,
        }

    sorted_lat = sorted(latencies_ms)
    n = len(sorted_lat)

    def percentile(pct: float) -> float:
        """Computes percentile using nearest-rank method."""
        idx = int(pct / 100.0 * n)
        idx = min(idx, n - 1)
        return round(sorted_lat[idx], 2)

    return {
        "avg_latency_ms": round(statistics.mean(sorted_lat), 2),
        "p50_latency_ms": percentile(50),
        "p95_latency_ms": percentile(95),
        "p99_latency_ms": percentile(99),
        "max_latency_ms": round(sorted_lat[-1], 2),
    }


def compute_efficiency_metrics(
    predictions: List[Dict[str, Any]],
    throughput_images_per_sec: Optional[float] = None,
    cpu_usage_percent: Optional[float] = None,
    memory_usage_mb: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Computes efficiency metrics from prediction entries and system stats.

    Latencies are extracted from prediction entries (inference_latency_ms field).
    Throughput and resource usage are provided externally (from monitoring).

    Args:
        predictions: List of prediction dicts (may have inference_latency_ms).
        throughput_images_per_sec: Measured throughput (if available).
        cpu_usage_percent: Average CPU usage (if available).
        memory_usage_mb: Peak memory usage (if available).

    Returns:
        Dict with all efficiency metric values.
    """
    # Extract latencies from predictions
    latencies = [
        p["inference_latency_ms"]
        for p in predictions
        if p.get("inference_latency_ms") is not None
    ]

    latency_stats = compute_latency_stats(latencies)

    result = {
        **latency_stats,
        "throughput_images_per_sec": throughput_images_per_sec,
        "cpu_usage_percent": cpu_usage_percent,
        "memory_usage_mb": memory_usage_mb,
    }

    logger.info(
        "Efficiency metrics: avg=%.1fms | p95=%.1fms | throughput=%s img/s",
        latency_stats["avg_latency_ms"],
        latency_stats["p95_latency_ms"],
        throughput_images_per_sec or "N/A",
    )

    return result
