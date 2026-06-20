# Operational Runbook

## Deployment Overview
- **Orchestration**: Containers are built dynamically via `SERVICE_NAME` args in the root `Dockerfile`.
- **CI/CD**: GitHub Actions (`.github/workflows/ci.yml`) runs Ruff linting and container smoke tests on every PR.

## Monitoring & Health
Monitor the overall system via the Observability service:
```bash
curl http://localhost:8010/observability/health
```
If any service reports `status: DOWN`, check the respective Docker container logs.

## Failure Scenarios & Recovery

### 1. Redis Queue Backpressure (Stuck Pipeline)
**Symptoms**: Ingestion succeeds, but the Dashboard UI shows no new cases.
**Action**:
1. Check Redis memory usage: `docker exec -it <redis-container> redis-cli info memory`
2. Check specific service logs (e.g., Detection or ANPR usually bottleneck first).
3. Scale the bottlenecked service by adding replicas in `docker-compose.yml`.

### 2. Database Unavailable
**Symptoms**: Evidence Generation or Dashboard APIs throw 500 errors.
**Action**:
1. Ensure `db` container is running: `docker ps | grep postgres`.
2. Check `DATABASE_URL` in `.env`.
3. Verify migrations: `alembic upgrade head`.

## Model Retraining & Updating
When accuracy drops, follow the Model Lifecycle flow:
1. **Intake**: Reviewers marking cases as "REJECT" automatically routes the artifact to the Retraining Backlog.
2. **Dataset Creation**: Call `POST /lifecycle/datasets/create?task=helmet-detection` to lock a new training batch.
3. **Promotion**: Once trained, register the new model metrics via `POST /lifecycle/models/register`.
4. **Staging**: Call `PUT /lifecycle/models/helmet_v2/status` with `{"status": "PRODUCTION"}`. The system enforces minimal thresholds (e.g., mAP > 0.75) before allowing promotion.
