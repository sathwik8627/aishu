# Aishu AI

A responsive AI assistant web app with text chat, browser voice recognition, a "Hey Aishu" wake phrase, and spoken replies. Flask keeps the OpenAI API key on the server.

## Run locally

Requirements: Python 3.10+, Google Chrome recommended, and an OpenAI API key with API billing enabled.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables before starting the app:

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_MODEL="gpt-4.1-mini"
python app.py
```

Open http://127.0.0.1:5000 in Chrome and allow microphone access. Click the glowing orb to enable voice mode, then say **"Hey Aishu"** followed by your question.

## Deploy on Render

1. Create a new **Web Service** and connect this GitHub repository.
2. Set **Build Command** to `pip install -r requirements.txt`.
3. Set **Start Command** to `gunicorn app:app`.
4. Add environment variable `OPENAI_API_KEY` with your API key. Optionally set `OPENAI_MODEL` to a model enabled for your API project.
5. Deploy.

Do not put the API key in frontend JavaScript or commit it to GitHub.

## Voice and browser limitations

- Wake phrase detection uses the browser Web Speech API. Chrome is recommended; support varies by browser and operating system.
- Keep the browser tab open and the device awake. A normal website cannot listen while the browser is closed or guarantee system-wide background listening.
- Female voice selection depends on voices installed in the browser/OS; Aishu selects a likely female English voice when available and otherwise uses the browser default.
- Microphone recognition may use the browser vendor's speech service.

## Security notes

This starter does not include user authentication, rate limiting, or per-user session isolation. Before exposing it publicly to multiple users, add those protections and monitor API usage. Keep the API key in the hosting provider's secret environment variables.

GitHub Pages cannot run this Flask backend or securely store the API key. Deploy the Flask app as a web service instead.
