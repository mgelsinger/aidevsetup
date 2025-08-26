import os
import httpx
from typing import List, Dict

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

# Ollama defaults
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# OpenAI defaults
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

class LLMClient:
    def __init__(self):
        self.provider = PROVIDER

    async def chat(self, messages: List[Dict[str, str]]) -> str:
        if self.provider == "openai":
            return await self._chat_openai(messages)
        # default to ollama
        return await self._chat_ollama(messages)

    async def _chat_ollama(self, messages: List[Dict[str, str]]) -> str:
        url = f"{OLLAMA_HOST}/api/chat"
        payload = {
            "model": OLLAMA_MODEL,
            "messages": messages,
            "stream": False
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            # Ollama returns an object with {message: {role, content}, ...}
            return data.get("message", {}).get("content", "")

    async def _chat_openai(self, messages: List[Dict[str, str]]) -> str:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set in environment (.env).")
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.2,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]