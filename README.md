# Member 1 — AI Agent & Conversation System

Starter implementation for the conversation/backend module of the
Adaptive Memory Evolution Framework project.

## What's here

| File | Responsibility |
|---|---|
| `main.py` | FastAPI backend, exposes `POST /chat` |
| `llm_connector.py` | Connects to the LLM (Anthropic or OpenAI) |
| `conversation_manager.py` | Combines retrieved memories with the query, generates the response |
| `memory_interface.py` | The contract with the Memory module (Member 2/3), plus a mock for testing |
| `requirements.txt` | Dependencies |

## Setup

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."   # or OPENAI_API_KEY if using OpenAI
uvicorn main:app --reload
```

## Test it

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_id": "u1", "message": "What did I tell you about my project last time?"}'
```

You should get back a JSON response. Because `MockMemoryStore` is wired in
by default, the model will see a couple of fake memories in its system
prompt — check the response reflects them.

## Switching LLM provider

In `main.py`:

```python
llm = LLMConnector(provider="anthropic", model="claude-sonnet-4-6")
# or
llm = LLMConnector(provider="openai", model="gpt-4o")
```

## Integrating with Member 2/3's memory module

Your two modules only need to agree on `memory_interface.py`. Once their
real memory store implements `MemoryStoreInterface` (both `retrieve_relevant`
and `store_interaction`), swap it in `main.py`:

```python
from real_memory_store import RealMemoryStore
memory_store = RealMemoryStore()   # instead of MockMemoryStore()
```

Nothing else in `conversation_manager.py` or `main.py` needs to change —
that's the whole point of coding against the interface first.

## Next steps beyond this starter

- Add conversation history persistence across restarts (currently in-memory only)
- Add authentication if multiple real users will hit the API
- Add a simple frontend (a chat widget, or even just a CLI loop) that calls `/chat`
- Add error handling for LLM API failures/timeouts
- Log token usage if your project needs to track cost
