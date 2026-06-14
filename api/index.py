"""
VisePanda v3.0.1 — China Travel AI
WSGI handler. Zero pip dependencies (stdlib only).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

THIS_DIR = Path(__file__).resolve().parent
ROOT = THIS_DIR.parent
DATA_DIR = ROOT / "data"
WEB_DIR = ROOT / "web"
STATIC_DIR = ROOT / "static"

# ── MIME types ──
MIME = {
    ".html": "text/html; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".webp": "image/webp",
    ".woff2": "font/woff2",
    ".txt": "text/plain; charset=utf-8",
}
TEXT_SUFFIXES = {".html", ".js", ".css", ".json", ".svg", ".txt"}

# ── LLM config (set via Vercel env vars) ──
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE = "https://api.deepseek.com/v1"


# ════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════

def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _json(start_response, payload: Any, status: str = "200 OK"):
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    start_response(status, [
        ("Content-Type", "application/json; charset=utf-8"),
        ("Content-Length", str(len(body))),
        ("Access-Control-Allow-Origin", "*"),
    ])
    return [body]


def _json_error(start_response, msg: str, status: str = "500 Internal Server Error"):
    return _json(start_response, {"error": msg}, status=status)


def _read_post(environ) -> dict:
    length = int(environ.get("CONTENT_LENGTH", "0") or "0")
    if length <= 0:
        return {}
    raw = environ["wsgi.input"].read(length)
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw) if raw else {}


def _load_json(path) -> dict | list | None:
    try:
        p = Path(path) if not isinstance(path, Path) else path
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return None


def _serve_static(start_response, request_path: str):
    """Serve files from web/ (frontend) and static/ (assets)."""
    if request_path in ("", "/"):
        rel = "index.html"
    else:
        rel = request_path.lstrip("/")

    # Try web/ first, then static/
    for base_dir in (WEB_DIR, STATIC_DIR):
        target = (base_dir / rel).resolve()
        if target.is_file() and _is_relative_to(target, base_dir.resolve()):
            body = target.read_bytes()
            ct = MIME.get(target.suffix, "application/octet-stream")
            headers = [
                ("Content-Type", ct),
                ("Content-Length", str(len(body))),
            ]
            # Cache static assets aggressively, not HTML
            if base_dir == STATIC_DIR or target.suffix not in (".html",):
                headers.append(("Cache-Control", "public, max-age=31536000, immutable"))
            else:
                headers.append(("Cache-Control", "public, max-age=300"))
            if target.suffix in TEXT_SUFFIXES:
                body = body.decode("utf-8").encode("utf-8")
            start_response("200 OK", headers)
            return [body]
    return None


def _sse_event(data: str, event: str = "message") -> bytes:
    """Format a Server-Sent Event."""
    return f"event: {event}\ndata: {data}\n\n".encode("utf-8")


# ════════════════════════════════════════════════════════════
# CHAT SSE ENDPOINT
# ════════════════════════════════════════════════════════════

def _handle_chat(environ, start_response):
    """POST /api/chat — SSE streaming chat with DeepSeek V4 Flash."""
    if not DEEPSEEK_API_KEY:
        return _json_error(start_response, "DEEPSEEK_API_KEY not configured", "503 Service Unavailable")

    params = _read_post(environ)
    messages = params.get("messages", [])
    if not messages:
        return _json_error(start_response, "messages required", "400 Bad Request")

    # Build system prompt with knowledge context
    system_prompt = _build_system_prompt(params)

    # Stream response via SSE
    def stream():
        import urllib.request

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        }
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": [{"role": "system", "content": system_prompt}] + messages,
            "stream": True,
            "temperature": 0.7,
            "max_tokens": 2048,
        }

        req = urllib.request.Request(
            f"{DEEPSEEK_BASE}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                buffer = ""
                while True:
                    chunk = resp.read(4096)
                    if not chunk:
                        break
                    buffer += chunk.decode("utf-8")
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # keep incomplete line

                    for line in lines:
                        line = line.strip()
                        if not line or line == "data: [DONE]":
                            continue
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                delta = data.get("choices", [{}])[0].get("delta", {})
                                content = delta.get("content", "")
                                if content:
                                    yield _sse_event(json.dumps({"token": content}))
                            except (json.JSONDecodeError, KeyError, IndexError):
                                pass
        except Exception as ex:
            yield _sse_event(json.dumps({"error": str(ex)}), event="error")

        yield _sse_event(json.dumps({"done": True}), event="done")

    headers = [
        ("Content-Type", "text/event-stream"),
        ("Cache-Control", "no-cache"),
        ("Connection", "keep-alive"),
        ("Access-Control-Allow-Origin", "*"),
        ("X-Accel-Buffering", "no"),
    ]
    start_response("200 OK", headers)
    return stream()


def _build_system_prompt(params: dict) -> str:
    """Build system prompt with optional city/tool knowledge context."""
    city = params.get("city", "")
    prompt_parts = [
        "You are VisePanda, an AI China travel planning expert. Help users plan trips within China.",
        "",
        "Your responses should be:",
        "- Practical and actionable (specific prices, transport times, restaurant names)",
        "- Structured with day-by-day itineraries when appropriate",
        "- Culturally aware (local customs, peak seasons, weather considerations)",
        "- Honest about what you know and don't know",
        "",
        "When suggesting itineraries, use this format:",
        "**Day 1: [Title]**",
        "- 🕐 Morning: [activity] at [location]",
        "- 🕐 Afternoon: [activity] at [location]",
        "- 🕐 Evening: [activity] at [location]",
        "- 🍽️ Eat: [specific restaurant/food]",
        "- 💡 Tip: [local advice]",
        "",
    ]
    if city:
        city_data = _load_json(DATA_DIR / "cities.json")
        if city_data and city in city_data:
            info = city_data[city]
            prompt_parts.append(f"## Knowledge: {city}")
            prompt_parts.append(json.dumps(info, ensure_ascii=False, indent=2))

    return "\n".join(prompt_parts)


# ════════════════════════════════════════════════════════════
# CITIES API
# ════════════════════════════════════════════════════════════

def _handle_cities(start_response, path: str):
    """GET /api/cities — list all cities. GET /api/cities/:city — city detail."""
    cities = _load_json(DATA_DIR / "cities.json")
    if cities is None:
        return _json_error(start_response, "City data not found")

    parts = path.strip("/").split("/")
    if len(parts) == 2:  # /api/cities
        # Return summary: name + brief info
        summary = {}
        for name, info in cities.items():
            summary[name] = {
                "name_cn": info.get("name_cn", ""),
                "best_season": info.get("best_season", ""),
                "days": info.get("days", ""),
                "highlights": info.get("highlights", [])[:3],
                "image": f"/static/img/city-{name.lower()}.jpg",
            }
        return _json(start_response, {"cities": summary})
    elif len(parts) == 3:  # /api/cities/beijing
        city_name = parts[2]
        if city_name in cities:
            return _json(start_response, {"city": cities[city_name]})
        return _json_error(start_response, f"City '{city_name}' not found", "404 Not Found")
    return _json_error(start_response, "Not found", "404 Not Found")


# ════════════════════════════════════════════════════════════
# TOOLS API
# ════════════════════════════════════════════════════════════

def _handle_tools(start_response, path: str):
    """GET /api/tools — list tools. GET /api/tools/:name — tool detail."""
    parts = path.strip("/").split("/")
    tool_name = parts[2] if len(parts) >= 3 else ""

    tools_index = {
        "packing": "Packing checklist by destination and season",
        "pricing": "Price estimates for transport/accommodation/food",
        "visa": "China visa guide for foreigners",
        "phrases": "Useful Chinese phrases for travelers",
        "emergency": "Emergency contacts and procedures in China",
    }

    if not tool_name:
        return _json(start_response, {"tools": tools_index})

    if tool_name in tools_index:
        data = _load_json(DATA_DIR / "tools.json")
        if data and tool_name in data:
            return _json(start_response, {"tool": data[tool_name]})
        return _json_error(start_response, f"Tool data '{tool_name}' not loaded", "500 Internal Server Error")

    return _json_error(start_response, f"Tool '{tool_name}' not found", "404 Not Found")


# ════════════════════════════════════════════════════════════
# WSGI APPLICATION
# ════════════════════════════════════════════════════════════

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/")
    method = environ.get("REQUEST_METHOD", "GET")

    # ── Health ──
    if path == "/api/health" and method == "GET":
        return _json(start_response, {
            "status": "alive",
            "version": "3.0.1",
            "build": "2026-06-14",
        })

    # ── Chat SSE ──
    if path == "/api/chat" and method == "POST":
        return _handle_chat(environ, start_response)

    # ── Cities API ──
    if path.startswith("/api/cities") and method == "GET":
        return _handle_cities(start_response, path)

    # ── Tools API ──
    if path.startswith("/api/tools") and method == "GET":
        return _handle_tools(start_response, path)

    # ── Static files (web/ + static/) ──
    result = _serve_static(start_response, path)
    if result is not None:
        return result

    # ── 404 fallback ──
    return _json_error(start_response, f"Not found: {path}", "404 Not Found")
