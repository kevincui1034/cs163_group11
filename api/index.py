"""
Vercel serverless entrypoint: exposes the Dash/Flask WSGI app as `app`.

The Dash app lives under `appengine/` and imports `components` / `pages`
relative to that directory, so we prepend `appengine` to sys.path before
importing `app`.
"""
from __future__ import annotations

import os
import sys

_APPENGINE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "appengine")
)
if _APPENGINE_DIR not in sys.path:
    sys.path.insert(0, _APPENGINE_DIR)

# Vercel's Python runtime expects a top-level WSGI/ASGI object named `app`.
from app import server as app  # noqa: E402

__all__ = ["app"]
