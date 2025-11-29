# Smart Trip Planner — Full Working Version (Minimal Production-Ready)

This project is a fully working starter for a Smart Trip Planner agent with a Streamlit UI.
It can run in two modes:
- MOCK mode (default): no OpenAI key required, returns deterministic example outputs.
- LLM mode: requires `OPENAI_API_KEY` environment variable; uses OpenAI ChatCompletions.

## Features
- Streamlit UI for entering trip preferences and viewing/exporting itinerary.
- Multi-agent structure (Recommender, Planner, Itinerary Builder) in code.
- Simple file-backed memory for user preferences and past trips.
- Local deterministic tools (distance estimator, cost estimator, iCal export).
- Exports: iCal file and CSV itinerary download.
- Clear prompts with JSON-schema-like expectations; robust JSON parsing and fallback.
- No Google APIs required.

## Quick start (mock)
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows (PowerShell)
pip install -r requirements.txt
streamlit run app/main.py
```

## Quick start (real LLM)
```bash
export OPENAI_API_KEY="sk-..."
streamlit run app/main.py --server.port 8501
```

## Project layout
```
smart_trip_planner_full/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ app/
   ├─ main.py
   ├─ agents.py
   ├─ tools.py
   ├─ memory.py
   ├─ ui.py
   ├─ exports.py
```

## Notes
- Do not commit API keys.
- This is a minimal but complete template; extend with real APIs (maps, bookings) later.
