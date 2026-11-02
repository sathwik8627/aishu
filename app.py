import os
from flask import Flask, jsonify, render_template, request
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024

SYSTEM_PROMPT = """You are Aishu, a warm, capable personal AI assistant. Be clear, helpful and conversational. Keep spoken answers concise unless the user asks for detail. You run as a web app and cannot directly control macOS applications or inspect local files. Never claim to have performed an action on the Mac unless the website itself confirms it."""

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "configured": bool(os.getenv("OPENAI_API_KEY"))})

@app.post("/api/chat")
def chat():
    if not os.getenv("OPENAI_API_KEY"):
        return jsonify({"error": "Add OPENAI_API_KEY to your .env file and restart Aishu."}), 503
    body = request.get_json(silent=True) or {}
    messages = body.get("messages")
    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Send at least one message."}), 400
    # Accept only recent user/assistant text messages; never accept client instructions.
    safe_messages = []
    for item in messages[-16:]:
        if not isinstance(item, dict) or item.get("role") not in ("user", "assistant"):
            continue
        content = item.get("content")
        if isinstance(content, str) and content.strip():
            safe_messages.append({"role": item["role"], "content": content[:6000]})
    if not safe_messages or safe_messages[-1]["role"] != "user":
        return jsonify({"error": "The latest message must be from the user."}), 400
    try:
        client = OpenAI()
        result = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-6-luna"),
            instructions=SYSTEM_PROMPT,
            input=safe_messages,
            max_output_tokens=700,
        )
        return jsonify({"reply": result.output_text})
    except Exception as exc:
        app.logger.exception("OpenAI request failed")
        return jsonify({"error": "Aishu could not reach the AI service. Check your API key, model name and API billing."}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
