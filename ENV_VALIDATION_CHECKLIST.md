# Environment Validation Checklist

> Run through this checklist before deploying or starting local development. Every item must pass before the system is considered ready.

---

## 1. PostgreSQL

| # | Check | Status |
|---|-------|--------|
| 1.1 | `DB_URL` environment variable is set | - [ ] Pass |
| 1.2 | PostgreSQL server is reachable on configured host:port | - [ ] Pass |
| 1.3 | Target database exists and user has CREATE/ALTER permissions | - [ ] Pass |
| 1.4 | Alembic migrations run without errors (`alembic upgrade head`) | - [ ] Pass |
| 1.5 | All 6 migration revisions (0001–0006) are applied | - [ ] Pass |
| 1.6 | Connection pool settings are appropriate for deployment target | - [ ] Pass |

---

## 2. Redis / Queue

| # | Check | Status |
|---|-------|--------|
| 2.1 | `REDIS_URL` or queue broker URL environment variable is set | - [ ] Pass |
| 2.2 | Redis/broker server is reachable on configured host:port | - [ ] Pass |
| 2.3 | All required topics exist or can be auto-created: `raw_frame`, `preprocessed_frame`, `detections`, `tracks`, `violations`, `anpr`, `incidents` | - [ ] Pass |
| 2.4 | Queue consumer groups are configured (if using Redis Streams) | - [ ] Pass |
| 2.5 | Pub/sub round-trip test succeeds (publish → consume → ack) | - [ ] Pass |

---

## 3. Object Storage

| # | Check | Status |
|---|-------|--------|
| 3.1 | `OBJECT_STORAGE_ROOT` environment variable is set | - [ ] Pass |
| 3.2 | Storage directory exists and is writable by the service user | - [ ] Pass |
| 3.3 | If using S3/GCS: bucket exists and credentials are valid | - [ ] Pass |
| 3.4 | Write + read round-trip test succeeds (save → retrieve → compare) | - [ ] Pass |
| 3.5 | Date-partitioned subdirectories can be auto-created (`YYYY/MM/DD`) | - [ ] Pass |

---

## 4. Model Paths

| # | Check | Status |
|---|-------|--------|
| 4.1 | `DETECTION_MODEL_PATH` is set and file exists | - [ ] Pass |
| 4.2 | `HELMET_MODEL_PATH` is set and file exists | - [ ] Pass |
| 4.3 | `PLATE_DETECTOR_MODEL_PATH` is set and file exists | - [ ] Pass |
| 4.4 | All model files are readable by the service user | - [ ] Pass |
| 4.5 | ONNX Runtime or required inference backend is installed | - [ ] Pass |
| 4.6 | Model input sizes match expected config (detection: 640×640, helmet: 64×64, plate: 320×320) | - [ ] Pass |

---

## 5. Service Ports

| # | Check | Service | Default Port | Status |
|---|-------|---------|-------------|--------|
| 5.1 | Ingestion service port is available | `ingestion` | 8001 | - [ ] Pass |
| 5.2 | Preprocessing service port is available | `preprocessing` | 8002 | - [ ] Pass |
| 5.3 | Detection service port is available | `detection` | 8003 | - [ ] Pass |
| 5.4 | Tracking service port is available | `tracking` | 8004 | - [ ] Pass |
| 5.5 | Rule engine service port is available | `rule-engine` | 8005 | - [ ] Pass |
| 5.6 | ANPR service port is available | `anpr` | 8006 | - [ ] Pass |
| 5.7 | Incident fusion service port is available | `incident-fusion` | 8007 | - [ ] Pass |
| 5.8 | Evidence service port is available | `evidence` | 8008 | - [ ] Pass |
| 5.9 | Dashboard API port is available | `dashboard-api` | 8009 | - [ ] Pass |
| 5.10 | Persistence / Alembic is not a running service | `persistence` | N/A | - [ ] Pass |
| 5.11 | All `/health` endpoints return `{"status": "ok"}` | all | — | - [ ] Pass |

---

## 6. Secrets & Credentials

| # | Check | Status |
|---|-------|--------|
| 6.1 | No secrets are hardcoded in source files | - [ ] Pass |
| 6.2 | `.env` file exists locally (and is in `.gitignore`) | - [ ] Pass |
| 6.3 | Database credentials are set via environment variables only | - [ ] Pass |
| 6.4 | Object storage credentials (if S3/GCS) are set via env or IAM roles | - [ ] Pass |
| 6.5 | API keys or tokens (if any) are stored in env vars, not in code | - [ ] Pass |
| 6.6 | CORS `allow_origins` is restricted in production (not `*`) | - [ ] Pass |

---

## Summary

| Section | Total Checks | Passed |
|---------|-------------|--------|
| PostgreSQL | 6 | __ / 6 |
| Redis / Queue | 5 | __ / 5 |
| Object Storage | 5 | __ / 5 |
| Model Paths | 6 | __ / 6 |
| Service Ports | 11 | __ / 11 |
| Secrets & Credentials | 6 | __ / 6 |
| **Total** | **39** | **__ / 39** |

> **All 39 checks must pass before the system is considered deployment-ready.**
