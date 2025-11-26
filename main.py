from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Ollama API URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Your local MedGemma model name
MODEL_NAME = "edwardlo12/medgemma-4b-it-Q4_K_M"

@app.get("/")
def home():
    return {"status": "Backend Running with Real MedGemma 🚀"}

@app.post("/ask")
async def ask_health(request: Request):
    data = await request.json()
    user_msg = data.get("question", "")

    payload = {
        "model": MODEL_NAME,
        "prompt": user_msg,
        "stream": False
    }

    resp = requests.post(OLLAMA_URL, json=payload)

    ai_reply = resp.json().get("response", "Model not responding")

    return {
        "your_question": user_msg,
        "ai_reply": ai_reply
    }
