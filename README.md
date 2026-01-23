# Assistly

Assistly is a lightweight, modular Python voice assistant framework. It combines intent classification, speech recognition and synthesis, and LLM integration to provide a set of simple skills (modules) that can be expanded.

## Key Features

- Intent classification via `core/intent_classifier.py`.
- Speech recognition and synthesis (voice in/out) via `core/recognizer.py` and `core/speech.py`.
- LLM client integration (`core/llm_client.py`) for smarter responses.
- A central router and skill system (`core/router.py`, `modules/`) to dispatch intents to modules.
- Built-in modules include: greeting, jokes, date/time, weather, news, location, search, open app/url, YouTube player, timer, and system info.
- Simple entry point: `main.py`.

## Project Layout

- `main.py` — starter/runner for the assistant.
- `core/` — core functionality: intent classification, recognition, LLM, routing, etc.
- `modules/` — individual skills (one file per skill).
- `requirements.txt` — Python dependencies.

## Quick Start

1. Install dependencies: `pip install -r requirements.txt`.
2. Run the assistant: `python main.py`.
