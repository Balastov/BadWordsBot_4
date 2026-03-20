import json
import time
import uuid
from pathlib import Path


DEBUG_LOG_PATH = Path("debug-f78a78.log")
DEBUG_SESSION_ID = "f78a78"


def debug_log(hypothesis_id: str, location: str, message: str, data: dict | None = None, run_id: str = "pre-fix") -> None:
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "id": f"log_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": data or {},
        "runId": run_id,
        "hypothesisId": hypothesis_id,
    }
    try:
        with DEBUG_LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        # Debug logging must never break bot runtime.
        pass
