# Changelog

## v3.0.3 (2026-06-15)
- **🗺️ Map Tab** — Full China overview map with all 36 cities plotted. Supports AMap (Gaode) when API key configured, with Leaflet fallback.
- **📍 All Cities Coordinates** — Expanded map data from 8 cities to all 36 cities with lat/lng coordinates.
- **📄 Documentation** — Added CHANGELOG.md, updated PLAN.md with version tracking.

## v3.0.2 (2026-06-14)
- **🔍 FAQ Knowledge Base** — 10-category FAQ matching engine. Vague user queries are now expanded with deep keywords and answer guidance injected into the LLM system prompt.
- **🏷️ Version Badge** — Dynamic version number displayed in header top-right corner and footer, fetched from `/api/health`.
- **🎯 FAQ Match Badge** — When a FAQ category is matched, a small badge appears above the AI response showing what was detected.

## v3.0.1 (2026-06-14)
- **Phase 3 Complete** — Map views, price estimates, smart trip validation.
- **Leaflet Maps** — City detail modals with dark-theme Leaflet maps, POI markers by category.
- **Trip Persistence** — Save/load/share itineraries via localStorage.
- **Responsive Design** — Full mobile/tablet/desktop support with dark/light themes.
- **36-City Knowledge Base** — Comprehensive data for 36 Chinese cities (food, hotels, tips, pricing).
- **SSE Streaming Chat** — Real-time streaming with DeepSeek V4 Flash.
- **WC26 Architecture** — Python WSGI + stdlib + Vercel deployment pattern.
