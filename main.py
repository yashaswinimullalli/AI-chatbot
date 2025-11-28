from fastapi import FastAPI, Request, HTTPException
import httpx   # make sure to install: pip install httpx

app = FastAPI()

# Ollama server URL
OLLAMA_URL = "http://localhost:11434/api/generate"

# Model name (must match what you pulled in Ollama)
MODEL_NAME = "edwardlo12/medgemma-4b-it-Q4_K_M"


@app.get("/")
def home():
    return {"status": "Backend is running with MedGemma "}


@app.post("/ask")
async def ask_health(request: Request):
    # Get user question
    body = await request.json()
    user_msg = body.get("question")

    if not user_msg:
        raise HTTPException(status_code=400, detail="Please send 'question' in the JSON body")

    payload = {
        "model": MODEL_NAME,
        "prompt": user_msg,
        "stream": False
    }

    # Send request to Ollama (ASYNC safe)
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(OLLAMA_URL, json=payload)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Cannot connect to Ollama: {e}")

    # Server returned non-OK
    if resp.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Ollama error: {resp.text}")

    data = resp.json()

    # Extract model reply
    ai_reply = data.get("response") or data

    return {
        "user_question": user_msg,
        "ai_reply": ai_reply
    }


