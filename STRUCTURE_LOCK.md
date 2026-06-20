# Structure Lock

> **Rule**: No extra top-level files or folders may be added to this repository without explicit approval. This document defines the canonical project layout.

## Approved Top-Level Folders

| Folder | Purpose |
|--------|---------|
| `libs/common-schemas/` | Shared Pydantic schemas and enums across all services |
| `libs/common-utils/` | Shared utility functions (time, IDs, paths, DB naming) |
| `libs/queue-contracts/` | Queue topic constants and envelope schemas |
| `libs/vision-utils/` | Shared computer vision helpers (image I/O, color, quality, bbox, crop, perspective) |
| `services/ingestion/` | Frame ingestion service (receive + store + publish) |
| `services/preprocessing/` | Frame quality analysis and enhancement service |
| `services/detection/` | Object detection inference service |
| `services/tracking/` | Multi-object tracking service |
| `services/rule-engine/` | Violation rule evaluation (helmet, speed, etc.) |
| `services/anpr/` | Automatic Number Plate Recognition service |
| `services/incident-fusion/` | Incident scoring, merging, and fusion service |
| `services/evidence/` | Evidence asset generation service |
| `services/dashboard-api/` | Dashboard REST API for frontend clients |
| `services/evaluation/` | Performance evaluation and benchmarking service |
| `services/persistence/` | Database models, migrations (Alembic), and session management |

## Approved Top-Level Files

| File | Purpose |
|------|---------|
| `TASK_LOG.md` | Checklist of all tasks executed against this repo |
| `STRUCTURE_LOCK.md` | This file — defines allowed structure |
| `README.md` | Project overview (if created) |
| `.gitignore` | Git ignore rules (if created) |
| `requirements.txt` | Python dependencies (if created) |
| `docker-compose.yml` | Container orchestration (if created) |

## Internal Service Structure Convention

Every service under `services/` follows this internal layout:

```
services/<service-name>/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI create_app() factory
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py        # register_routes(app)
│   │   └── endpoints.py     # Route handlers (thin, delegate to services)
│   └── services/
│       ├── __init__.py
│       └── *.py              # Business logic modules
└── tests/
    └── __init__.py
```

## Rules

1. **No new top-level folders** may be created without updating this file and obtaining explicit approval.
2. **No new services** may be added under `services/` without updating this file.
3. **No new libs** may be added under `libs/` without updating this file.
4. **One file per table group** for DB models (not one file per field, not all in one file).
5. **One migration per table group** (not one giant migration for everything).
6. **Endpoints must be thin** — all business logic lives in the `services/` layer.
7. **Orchestrator functions** call separated helpers; they do not reimplement logic.
