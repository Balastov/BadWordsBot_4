import json
import os
import time
import uuid
from pathlib import Path


DEBUG_LOG_PATH = Path("debug-f78a78.log")
DEBUG_SESSION_ID = "f78a78"
DEBUG_LOG_FALLBACK_PATH = Path("/tmp/debug-f78a78.log")


def debug_log(hypothesis_id: str, location: str, message: str, data: dict | None = None, run_id: str = "pre-fix") -> None:
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "id": f"log_{int(time.time() * 1000)}_{uuid.uuid4().hex[:8]}",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": {
            **(data or {}),
            "cwd": os.getcwd(),
        },
        "runId": run_id,
        "hypothesisId": hypothesis_id,
    }
    targets = [DEBUG_LOG_PATH, DEBUG_LOG_FALLBACK_PATH]
    for target in targets:
        try:
            with target.open("a", encoding="utf-8") as f:
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            break
        except Exception:
            continue
