# Developer Guide

## Local Setup

1. **Clone & Environment:**
   ```bash
   git clone <repo-url>
   cd traffic-management-system
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Environment Variables:**
   ```bash
   cp .env.example .env
   ```

## Running the System

### Option A: Full Infrastructure (Docker Compose)
Spins up PostgreSQL, Redis, and all microservices.
```bash
docker-compose up --build
```
Access the frontend UI at: `http://localhost:8000/static/index.html` (Assuming frontend mapped to 8000).

### Option B: Local Development (Single Service)
To run a single service (e.g., `ingestion`) natively with hot-reloading:
```bash
uvicorn services.ingestion.app.main:app --reload --port 8001
```

## Running Tests
We maintain an End-to-End integration suite that mocks queue boundaries to validate data consistency.
```bash
pytest tests/e2e/test_end_to_end.py -v
```

## Extending the System (Adding a New Violation)
To add a new rule (e.g., "Triple Riding"):
1. Create a new service directory: `services/triple_riding_rule/`.
2. Subscribe to the `tracking` queue output.
3. Apply spatial logic to count bounding boxes per motorcycle track.
4. If violation condition met = publish candidate to the existing `ANPR` queue.
