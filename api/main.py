"""
VisePanda v2 — Clean rewrite.
Backend-rendered HTML. Supabase config injected server-side.
No async config fetching, no __API_BASE__ hacks.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import uuid
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from jose import jwt
from pydantic import BaseModel
from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

# ═══════════════════════════════════════════════════════════════
# DB
# ═══════════════════════════════════════════════════════════════

DB_URL = os.getenv("DATABASE_URL", "sqlite:///data.sqlite3")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def _uid():
    return str(uuid.uuid4())


def _now():
    return dt.datetime.now(dt.timezone.utc)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uid)
    profile: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Trip(Base):
    __tablename__ = "trips"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uid)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), index=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    cities: Mapped[list] = mapped_column(JSON, default=list)
    itinerary: Mapped[dict] = mapped_column(JSON, default=dict)
    constraints: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


class Message(Base):
    __tablename__ = "messages"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=_uid)
    trip_id: Mapped[str] = mapped_column(String, ForeignKey("trips.id"), index=True)
    user_id: Mapped[str] = mapped_column(String, index=True)
    role: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), default=_now, index=True)


# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════

def _env(key, fallback=""):
    return os.getenv(key, fallback).strip()


SUPABASE_URL = _env("SUPABASE_URL") or _env("NEXT_PUBLIC_SUPABASE_URL") or _env("VITE_SUPABASE_URL")
SUPABASE_ANON_KEY = _env("SUPABASE_ANON_KEY") or _env("NEXT_PUBLIC_SUPABASE_ANON_KEY") or _env("VITE_SUPABASE_ANON_KEY")
LLM_URL = _env("LLM_BASE_URL", "https://api.deepseek.com")
LLM_KEY = _env("LLM_API_KEY")
LLM_MODEL = _env("LLM_MODEL", "deepseek-v4-flash")
AUTH_BYPASS = _env("AUTH_TEST_BYPASS") == "1"
IS_DEV = bool(_env("IS_DEV"))

# ═══════════════════════════════════════════════════════════════
# Auth
# ═══════════════════════════════════════════════════════════════

_JWKS_CACHE: dict = {"ts": 0.0, "jwks": None}


def _get_jwks():
    now = time.time()
    if _JWKS_CACHE["jwks"] and (now - _JWKS_CACHE["ts"]) < 300:
        return _JWKS_CACHE["jwks"]
    r = httpx.get(f"{SUPABASE_URL}/auth/v1/certs", timeout=10)
    r.raise_for_status()
    _JWKS_CACHE["jwks"] = r.json()
    _JWKS_CACHE["ts"] = now
    return _JWKS_CACHE["jwks"]


def _verify_token(token: str) -> dict:
    if AUTH_BYPASS and token.startswith("test:"):
        return {"sub": token.split(":", 1)[1].strip() or "test_user"}
    header = jwt.get_unverified_header(token)
    kid = header.get("kid")
    if not kid:
        raise HTTPException(401, "Invalid token")
    jwks = _get_jwks()
    key = next((k for k in jwks.get("keys", []) if k.get("kid") == kid), None)
    if not key:
        raise HTTPException(401, "Unknown key")
    return jwt.decode(token, key, algorithms=["RS256"], audience=_env("SUPABASE_JWT_AUD") or None,
                      options={"verify_aud": bool(_env("SUPABASE_JWT_AUD"))})


def _principal(request: Request) -> tuple[str, str]:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        claims = _verify_token(token)
        return "user", claims["sub"]
    raise HTTPException(401, "Login required")


def _get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════
# HTML Templates
# ═══════════════════════════════════════════════════════════════

import time

def _html_page(title: str, body: str, head_extra: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
{head_extra}
<style>
:root{{--bg:#05070b;--bg2:#0a0f17;--ln:rgba(255,255,255,.08);--m:rgba(255,255,255,.62);--t:rgba(255,255,255,.92);--a:#7dd3fc;font-family:system-ui,sans-serif}}
body{{margin:0;min-height:100vh;background:radial-gradient(1200px 800px at 30% 15%,#121826 0%,var(--bg2) 55%,var(--bg) 100%);color:var(--t)}}
header{{height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 16px;border-bottom:1px solid var(--ln);background:rgba(8,10,14,.55);backdrop-filter:blur(10px)}}
.brand{{display:flex;gap:10px;align-items:center;font-weight:650;font-size:14px}}
.dot{{width:10px;height:10px;border-radius:99px;background:var(--a);box-shadow:0 0 18px rgba(125,211,252,.45)}}
.btn{{font-size:12px;padding:8px 16px;border-radius:999px;border:1px solid var(--ln);background:rgba(255,255,255,.04);color:var(--t);cursor:pointer;text-decoration:none}}
.btn:hover{{background:rgba(255,255,255,.08)}}
.btn-p{{background:rgba(125,211,252,.14);border-color:rgba(125,211,252,.25)}}
.btn-p:hover{{background:rgba(125,211,252,.22)}}
main{{max-width:720px;margin:0 auto;padding:40px 16px 80px;text-align:center}}
.hero{{margin-top:60px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 10px}}
.sub{{color:var(--m);margin:0 0 22px;line-height:1.5}}
.input-wrap{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}
input{{height:48px;border-radius:999px;border:1px solid var(--ln);background:rgba(255,255,255,.03);color:var(--t);padding:0 16px;outline:none;width:min(500px,80vw)}}
input:focus{{border-color:rgba(125,211,252,.35);box-shadow:0 0 0 4px rgba(125,211,252,.12)}}
.chat-wrap{{display:flex;flex-direction:column;height:calc(100vh - 56px)}}
#messages{{flex:1;overflow-y:auto;padding:16px}}
.msg{{margin:8px 0;max-width:85%}}
.msg.user{{margin-left:auto;text-align:right}}
.bubble{{display:inline-block;padding:10px 14px;border-radius:14px;border:1px solid var(--ln);background:rgba(255,255,255,.03);line-height:1.4;white-space:pre-wrap}}
.msg.user .bubble{{background:rgba(125,211,252,.10);border-color:rgba(125,211,252,.18)}}
.chat-footer{{padding:12px 16px;border-top:1px solid var(--ln);background:rgba(8,10,14,.55)}}
.chat-footer form{{display:flex;gap:10px}}
.chat-footer input{{flex:1}}
.error{{color:#fca5a5;padding:20px;text-align:center}}
footer{{position:fixed;bottom:0;left:0;right:0;padding:10px 16px;border-top:1px solid var(--ln);background:rgba(8,10,14,.45);backdrop-filter:blur(10px);font-size:12px;color:var(--m)}}
</style>
</head>
<body>
{body}
</body>
</html>"""


def _auth_ui(user_id: str | None) -> str:
    if user_id:
        return f'<span style="font-size:12px;padding:6px 10px;border:1px solid var(--ln);border-radius:999px">✓ Signed in</span> <a href="/logout" class="btn">Sign out</a>'
    return '<button class="btn btn-p" onclick="window._signIn()">Sign in with Google</button>'


def _supabase_js() -> str:
    return f"""<script src="https://esm.sh/@supabase/supabase-js@2"></script>
<script>
const SUPABASE_URL = "{SUPABASE_URL}";
const SUPABASE_KEY = "{SUPABASE_ANON_KEY}";
let _sb = null;

function getSb() {{
  if (_sb) return _sb;
  if (!SUPABASE_URL || !SUPABASE_KEY) return null;
  _sb = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  return _sb;
}}

async function getSession() {{
  const sb = getSb();
  if (!sb) return null;
  const {{ data }} = await sb.auth.getSession();
  return data.session || null;
}}

window._signIn = async function() {{
  const sb = getSb();
  if (!sb) {{ alert("Supabase not configured"); return; }}
  await sb.auth.signInWithOAuth({{ provider: "google", options: {{ redirectTo: location.origin + "/callback" }} }});
}};

window._signOut = async function() {{
  const sb = getSb();
  if (sb) await sb.auth.signOut();
  location.href = "/";
}};
</script>"""


# ═══════════════════════════════════════════════════════════════
# App
# ═══════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="VisePanda", version="2.0.0", lifespan=lifespan)

if IS_DEV:
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ── Pages ─────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user_id = None
    try:
        _, user_id = _principal(request)
    except HTTPException:
        pass

    return _html_page("VisePanda — China Travel Agent", f"""
<header>
  <div class="brand"><div class="dot"></div>VisePanda</div>
  <div>{_auth_ui(user_id)}</div>
</header>
<main>
  <div class="hero">
    <h1>Plan your China trip</h1>
    <p class="sub">Chat with AI to build your itinerary. Hotels, tickets, local tips — all in one place.</p>
    <form class="input-wrap" onsubmit="go(event)">
      <input id="q" placeholder="e.g. Beijing 5 days, food + history">
      <button class="btn btn-p" type="submit">Start →</button>
    </form>
  </div>
</main>
<footer>Supports EN · 中文 · Русский · Español · العربية · 한국어 · 日本語 · Français · Deutsch</footer>
{_supabase_js()}
<script>
function go(e){{ e.preventDefault(); const v=document.getElementById("q").value.trim(); const id="t_"+crypto.randomUUID(); const u="/chat?trip="+id; location.href=v?u+"&q="+encodeURIComponent(v):u; }}
</script>
""")


@app.get("/callback", response_class=HTMLResponse)
def callback():
    return _html_page("Signing in…", """
<main style="margin-top:120px">
  <h1>Signing in…</h1>
  <p class="sub">You'll be redirected shortly.</p>
</main>
""" + _supabase_js() + """
<script>
(async () => {
  const sb = getSb();
  if (!sb) { document.querySelector("h1").textContent = "Error: Supabase not configured"; return; }
  const { data, error } = await sb.auth.getSessionFromUrl();
  if (error) { document.querySelector("h1").textContent = "Sign-in failed"; document.querySelector(".sub").textContent = error.message; return; }
  if (data.session) { location.href = "/"; }
})();
</script>
""")


@app.post("/logout")
def logout():
    return HTMLResponse("""<script>
(async () => {
  const sb = window.opener ? null : (window.supabase ? window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY) : null);
  if (sb) await sb.auth.signOut();
  location.href = "/";
})();
</script>""")


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request, trip: str = "", q: str = ""):
    user_id = None
    try:
        _, user_id = _principal(request)
    except HTTPException:
        pass

    trip_id = trip or f"t_{uuid.uuid4()}"

    return _html_page("Chat · VisePanda", f"""
<header>
  <div class="brand"><div class="dot"></div>VisePanda</div>
  <div><a href="/" class="btn">Home</a> {_auth_ui(user_id)}</div>
</header>
<div class="chat-wrap">
  <div id="messages"></div>
  <div class="chat-footer">
    <form onsubmit="sendMsg(event)">
      <input id="msgInput" placeholder="Type a message…" autofocus>
      <button class="btn btn-p" type="submit">Send</button>
    </form>
  </div>
</div>
{_supabase_js()}
<script>
const TRIP_ID = "{trip_id}";
const INITIAL_Q = {json.dumps(q)};

async function api(path, opts={{}}) {{
  const session = await getSession();
  const headers = {{ ...(opts.headers || {{}}), "Content-Type": "application/json" }};
  if (session?.access_token) headers["Authorization"] = "Bearer " + session.access_token;
  return fetch(path, {{ ...opts, headers, body: opts.body ? JSON.stringify(opts.body) : undefined }});
}}

function addMsg(role, text) {{
  const d = document.createElement("div");
  d.className = "msg " + (role === "user" ? "user" : "bot");
  d.innerHTML = '<div class="bubble">' + text.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\\n/g,"<br>") + '</div>';
  document.getElementById("messages").appendChild(d);
  document.getElementById("messages").scrollTop = 1e9;
}}

async function sendMsg(e) {{
  e.preventDefault();
  const input = document.getElementById("msgInput");
  const text = input.value.trim();
  if (!text) return;
  input.value = "";
  addMsg("user", text);

  const r = await api("/api/chat", {{ method: "POST", body: {{ trip_id: TRIP_ID, text }} }});
  const data = await r.json();
  addMsg("bot", data.reply || "(no response)");
}}

if (INITIAL_Q) {{ document.getElementById("msgInput").value = INITIAL_Q; sendMsg(new Event("submit")); }}
</script>
""")


# ── API ───────────────────────────────────────────────────────

@app.get("/api/health")
def health():
    return {"ok": True, "ts": time.time()}


@app.post("/api/chat")
def api_chat(payload: dict, request: Request):
    user_id = "guest"
    try:
        _, user_id = _principal(request)
    except HTTPException:
        pass

    db = SessionLocal()
    try:
        trip_id = payload.get("trip_id", "")
        text = payload.get("text", "")
        history = payload.get("history", [])

        # Ensure user
        user = db.query(User).filter(User.id == user_id).one_or_none()
        if not user:
            user = User(id=user_id)
            db.add(user)

        # Ensure trip
        trip = db.query(Trip).filter(Trip.id == trip_id).one_or_none()
        if not trip:
            trip = Trip(id=trip_id, user_id=user_id)
            db.add(trip)

        # Save user message
        db.add(Message(trip_id=trip_id, user_id=user_id, role="user", content=text))

        # Call LLM
        reply = _call_llm(history, text)

        # Save assistant message
        db.add(Message(trip_id=trip_id, user_id=user_id, role="assistant", content=reply))

        trip.updated_at = _now()
        if not trip.title and len(text) < 50:
            trip.title = text

        db.commit()
        return {"reply": reply, "trip": {"id": trip.id, "title": trip.title}}
    finally:
        db.close()


def _call_llm(history: list, text: str) -> str:
    if not LLM_KEY:
        return "Hi! I'm VisePanda, your China travel assistant. What city are you planning to visit?"

    messages = [{"role": "system", "content": "You are VisePanda, a helpful China travel assistant. Be concise, warm, and practical. Suggest specific places and tips. Respond in the same language the user writes in."}]
    messages.extend(history[-20:])
    messages.append({"role": "user", "content": text})

    try:
        r = httpx.post(
            f"{LLM_URL}/chat/completions",
            headers={"Authorization": f"Bearer {LLM_KEY}"},
            json={"model": LLM_MODEL, "messages": messages, "temperature": 0.7, "max_tokens": 1024},
            timeout=25,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Sorry, I'm having trouble connecting. Please try again. ({str(e)[:100]})"


# ═══════════════════════════════════════════════════════════════
# Entrypoint
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
