# medgemma_client.py
import httpx
import asyncio

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "edwardlo12/medgemma-4b-it-Q4_K_M"

async def call_medgemma_text(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "No response from MedGemma")

async def call_medgemma_image(image_path: str, context: str = "") -> str:
    prompt = f"Analyze this image: {image_path}. Context: {context}"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(OLLAMA_URL, json=payload)
        r.raise_for_status()
        data = r.json()
        return data.get("response", "No response from MedGemma")
