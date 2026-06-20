# API Overview

## 1. Ingestion API (Edge -> Backend)
**POST** `/ingest/frame`
Receives raw base64 frames from edge traffic cameras.

**Request Payload:**
```json
{
  "camera_id": "cam-northex-01",
  "timestamp": "2026-06-19T10:00:00Z",
  "image_data_base64": "iVBORw0KGgo...",
  "metadata": {"zone": "North"}
}
```
**Response:** `{"status": "success", "trace_id": "uuid..."}`

## 2. Dashboard API (Backend -> UI)
**GET** `/incidents?status=OPEN`
Retrieves the review queue.

**POST** `/incidents/{incident_id}/review`
Submits a human decision.

**Request Payload:**
```json
{
  "reviewer_id": "rev_01",
  "action": "APPROVE", 
  "notes": "Clear visibility of no helmet"
}
```
**Response:** `{"status": "success", "data": {"new_status": "APPROVED"}}`

## 3. Observability API
**GET** `/observability/health`
Aggregates health checks of all internal services and database connections.
