# AI Dev Sandbox (Windows) — Bootstrap Template

A reproducible **Windows-first AI development template** you can spin up in any empty folder with **one PowerShell command**. Works with **Ollama (local)** or **OpenAI API** behind a tiny **FastAPI** server.

---

## Features
- Per-project **Python virtual environment** (`.venv`)
- **Provider-switchable** LLM client:
  - **Ollama** (local)
  - **OpenAI** (cloud)
- Minimal **FastAPI** server with `/v1/chat` and `/health`
- One-shot **PowerShell bootstrap** + helper scripts
- Includes a **smoke test** (`test.ps1`)

---

## Quick Start (Windows + PowerShell)

1. Unzip this template into an **empty folder**.
2. Open PowerShell in that folder and run:
   
   ```powershell
   .\bootstrap.ps1
   ```
   
   This creates `.venv`, installs dependencies, and copies `.env.example` → `.env` (if missing).

3. Start the API server:
   ```powershell
   .\run.ps1
   ```

4. Smoke test:
   ```powershell
   .\test.ps1
   ```

Docs are at **http://127.0.0.1:8000/docs**.

---

## Configuration

Edit `.env` to choose your provider and models:

```ini
# Provider can be: ollama | openai
PROVIDER=ollama

# --- Ollama (local) ---
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.1

# --- OpenAI ---
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-4o-mini
```

- **Ollama**: Install and run Ollama locally, and pull a model at least once (e.g. `ollama run llama3.1`).
- **OpenAI**: Add your API key and set a model your account supports.

---

## API

### POST `/v1/chat`
**Request**
```json
{"messages":[{"role":"user","content":"Hello!"}]}
```
**Response**
```json
{"role":"assistant","content":"Hi there!"}
```

### GET `/health`
**Response**
```json
{"status":"ok","provider":"ollama"}
```

---

## Project Structure

```
app/
  llm_client.py    # provider-switchable client (Ollama or OpenAI) using httpx
  schemas.py       # Pydantic models for requests/responses
  server.py        # FastAPI app with /v1/chat and /health
bootstrap.ps1      # create .venv, install deps, set up .env
run.ps1            # start the FastAPI server (uvicorn --reload)
test.ps1           # smoke test the /v1/chat endpoint
requirements.txt
.env.example
.gitignore
```

---

## Scripts Reference

- `.\bootstrap.ps1` — Creates/refreshes `.venv`, installs `requirements.txt`, ensures `.env` exists.
- `.\run.ps1` — Launches `uvicorn app.server:app --reload` at `http://127.0.0.1:8000`.
- `.\test.ps1` — Sends a simple chat request to `/v1/chat` and prints the JSON response.

---

## Troubleshooting

- **`python` not found**: Install Python 3.10+ and reopen PowerShell.
- **`No .venv found`**: Run `.\bootstrap.ps1` first.
- **Ollama errors**: Ensure the daemon is running and the model name matches `OLLAMA_MODEL`.
- **OpenAI errors**: Verify `OPENAI_API_KEY` and your chosen model’s availability.

---

## License

MIT — use, modify, and share freely.
