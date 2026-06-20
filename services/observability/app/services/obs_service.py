import logging
from typing import Dict, Any, List

# MOCK: If TSDB (e.g., Prometheus/Postgres) is not ready, we mock the stores here.
# from services.persistence.app.db.session import get_db

logger = logging.getLogger(__name__)

# Mocked trace store (grouped by trace_id)
_trace_store: Dict[str, List[Dict[str, Any]]] = {}

# Mocked metrics aggregation state
_metrics_state: Dict[str, Dict[str, Any]] = {}

# Alerting thresholds
LATENCY_THRESHOLD_MS = 5000
LOW_CONFIDENCE_THRESHOLD = 0.6

async def record_pipeline_event(event_data: Any) -> Dict[str, Any]:
    """
    Records a pipeline event, updates running metrics, and evaluates alerts.
    """
    trace_id = event_data.trace_id
    service_name = event_data.service_name
    
    # 1. Store Audit Trace (MOCKED TSDB / DB)
    record = event_data.model_dump()
    if trace_id not in _trace_store:
        _trace_store[trace_id] = []
    _trace_store[trace_id].append(record)
    
    # 2. Update Aggregated Metrics (MOCKED Prometheus Counter/Gauge)
    if service_name not in _metrics_state:
        _metrics_state[service_name] = {
            "total_events": 0, "failures": 0, 
            "total_latency": 0, "low_confidence_count": 0
        }
        
    state = _metrics_state[service_name]
    state["total_events"] += 1
    
    if event_data.status == "FAILED":
        state["failures"] += 1
        
    if event_data.latency_ms is not None:
        state["total_latency"] += event_data.latency_ms
        
    if event_data.confidence_score is not None and event_data.confidence_score < LOW_CONFIDENCE_THRESHOLD:
        state["low_confidence_count"] += 1

    # 3. Evaluate Thresholds & Emit Alerts (MOCKED AlertManager)
    alert_emitted = None
    if event_data.latency_ms is not None and event_data.latency_ms > LATENCY_THRESHOLD_MS:
        alert_emitted = f"HIGH_LATENCY in {service_name}: {event_data.latency_ms}ms"
        logger.warning(f"ALERT TRIGGERED: {alert_emitted} | Trace: {trace_id}")
        # In production, publish this to an Alerting/Slack queue
        
    if event_data.status == "FAILED":
        alert_emitted = f"PIPELINE_FAILURE in {service_name}"
        logger.error(f"ALERT TRIGGERED: {alert_emitted} | Trace: {trace_id}")

    logger.info(f"Recorded observability event for trace {trace_id} from {service_name}")
    
    return {
        "trace_id": trace_id,
        "recorded": True,
        "alert_triggered": alert_emitted
    }

async def fetch_trace_history(trace_id: str) -> List[Dict[str, Any]]:
    """Retrieves the chronological audit logs for a given trace_id."""
    events = _trace_store.get(trace_id, [])
    # Sort chronologically
    return sorted(events, key=lambda x: x["timestamp"])

async def generate_monitoring_summary() -> Dict[str, Any]:
    """Computes high-level health and stage metrics."""
    stage_metrics = {}
    active_alerts = []
    
    for service_name, state in _metrics_state.items():
        total = state["total_events"]
        failures = state["failures"]
        
        failure_rate = (failures / total) if total > 0 else 0.0
        avg_latency = (state["total_latency"] / total) if total > 0 else 0.0
        
        stage_metrics[service_name] = {
            "total_events": total,
            "failure_rate": round(failure_rate, 4),
            "avg_latency_ms": round(avg_latency, 2),
            "low_confidence_count": state["low_confidence_count"]
        }
        
        if failure_rate > 0.05:  # Arbitrary 5% error budget threshold
            active_alerts.append(f"High failure rate ({failure_rate:.1%}) in {service_name}")
            
    system_health = "DEGRADED" if active_alerts else "HEALTHY"
    
    return {
        "system_health": system_health,
        "active_alerts": active_alerts,
        "stage_metrics": stage_metrics
    }
