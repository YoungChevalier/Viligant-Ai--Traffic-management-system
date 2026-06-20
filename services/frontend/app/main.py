import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Traffic Reviewer UI")

# Ensure static dir exists for mounting
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount the static directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

INDEX_PATH = os.path.join(STATIC_DIR, "index.html")

@app.get("/")
async def serve_spa():
    """Serves the SPA index page."""
    return FileResponse(INDEX_PATH)

@app.get("/{full_path:path}")
async def spa_catch_all(full_path: str):
    """
    SPA catch-all: any path that doesn't match /static/* serves index.html.
    This allows hash-based routing (#dashboard, #cases, etc.) to work
    even if the user navigates directly to a path like /cases.
    """
    # If the path points to an actual static file, let the mount handle it
    requested = os.path.join(STATIC_DIR, full_path)
    if os.path.isfile(requested):
        return FileResponse(requested)
    return FileResponse(INDEX_PATH)
