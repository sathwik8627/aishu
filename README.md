# Aishu AI

A responsive, local-first web interface for a personal AI assistant. The Flask backend keeps the OpenAI API key on the server; the browser provides chat, browser speech recognition wake-word detection, and speech synthesis.

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.10+
- Google Chrome recommended for Web Speech API voice recognition
- An OpenAI API key with API billing enabled

## Run locally

```bash
cd aishu-ai-website
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set `OPENAI_API_KEY`. The default model is `gpt-6-luna`; change `OPENAI_MODEL` to a model enabled for your API project if needed.

```bash
python app.py
```

Open <http://127.0.0.1:5000> in Chrome. Allow microphone access, click the glowing orb to enable voice mode, then say **“Hey Aishu”** followed by your question. Keep the tab open and the Mac awake for wake-word listening.

## Voice and browser limitations

- Wake phrase detection is implemented in the browser using the Web Speech API and checks recognized speech for “Hey Aishu”. It is not a dedicated low-level wake-word engine.
- Browser speech recognition support varies. Chrome on macOS is recommended; Safari may not support the required continuous recognition behavior.
- A website cannot listen while the browser is closed, guarantee background listening, or directly launch native Mac apps. For system-wide always-on wake-word detection and Mac controls, build a signed native macOS companion app.
- Speech recognition may use the browser vendor's recognition service. Recognized text is sent to the local Flask backend, then to OpenAI for responses.
- Female voice selection depends on voices installed in the browser/OS. The app selects a likely female English voice when available and otherwise uses the browser default.

## Security

- Never commit `.env` or expose your API key in frontend JavaScript.
- This starter is intended for local use. Before public deployment, add authentication, rate limiting, HTTPS, CSRF protection, and per-user session isolation.
- Do not deploy the Flask backend with the development server. Use a production WSGI server such as Gunicorn or Waitress.

## GitHub Pages

GitHub Pages can host only the static frontend. It cannot run this Flask backend or securely hold an OpenAI API key. To make Aishu available publicly, deploy the backend separately and configure a protected frontend API URL, or keep the app local on your Mac.
