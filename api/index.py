"""
Vercel serverless entrypoint: exposes the Dash/Flask WSGI app as `app`.

The Dash app lives under `appengine/` and imports `components` / `pages`
relative to that directory, so we prepend `appengine` to sys.path before
importing `app`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_APPENGINE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "appengine")
)
if _APPENGINE_DIR not in sys.path:
    sys.path.insert(0, _APPENGINE_DIR)


def _fail_fast_if_local_data_missing() -> None:
    """Clear error in Vercel logs when USE_GCS=0 but data files were not deployed."""
    if os.environ.get("USE_GCS", "0") == "1":
        return
    data_dir = Path(_APPENGINE_DIR) / "components" / "data"
    for name in ("Pokemon.csv", "gen9ou_full_data.json"):
        path = data_dir / name
        if not path.is_file():
            raise FileNotFoundError(
                f"Missing data file for local mode: {path}. "
                "Commit these files under appengine/components/data/ or set USE_GCS=1 "
                "with BUCKET_NAME and GCP_SERVICE_ACCOUNT_JSON."
            )


_fail_fast_if_local_data_missing()

# Vercel's Python runtime expects a top-level WSGI/ASGI object named `app`.
from app import server as app  # noqa: E402

__all__ = ["app"]
