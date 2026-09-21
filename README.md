# roleplay-agent

A compact, readable **single-agent runtime**: persona switching, tool calling,
and a token-budgeted memory that compresses itself with an LLM summary. ~150
lines of Python, no framework — the point is to see the whole agent loop end to
end, not to hide it behind abstractions.

Talks to any OpenAI-compatible endpoint (defaults to Moonshot / Kimi).

## The agent loop

```
user input
  └─> build messages: system(persona) + memory.recent() + user turn
        └─> LLM.generate(messages, tools)
              ├─ tool_calls?  ──> execute_tool(name, json.loads(args))
              │                    └─> feed result back, regenerate
              └─ plain text   ──> print
  └─> memory.add(user), memory.add(assistant)
        └─ over token budget? ──> summarize into long-term memory, clear short-term
```

Two design choices worth calling out:

* **Memory that bounds itself.** `core/memory.py` counts tokens with `tiktoken`
  against a budget; when short-term history overflows it rolls the transcript
  into a running long-term *summary* (produced by the model itself) and resets
  the short-term buffer. This is the cheap, real version of the context-window
  management every agent eventually needs.
* **Persona as swappable system prompt.** `core/persona.py` keeps a small map of
  roles; `/role <name>` hot-swaps the system prompt at runtime without touching
  conversation state.

## Layout

```
app.py            interactive REPL: persona + memory + tool-call loop
core/llm.py       thin OpenAI-compatible client (Moonshot base URL)
core/memory.py    token-budgeted short-term + LLM-summarized long-term memory
core/persona.py   switchable system-prompt roles
core/tools.py     tool schema + dispatcher (sample get_weather)
core/agent_core.py  headless RolePlayAgent wrapper for non-REPL use
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env          # put your own Moonshot key in .env
python app.py
```

`.env` is git-ignored. Do not commit real keys.

```
You: hi
Agent: ...
You: /role programmer
Switched to programmer
```

## Scope & honesty

This is a **minimal, single-agent loop** — one user turn at a time, one tool per
response, an in-memory store that resets on restart. It is meant as a legible
reference implementation of the persona/memory/tool-call pattern, not a
production agent framework. The sample `get_weather` tool is a stub.

## License

MIT
