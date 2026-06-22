<p align="center">
  <img src="assets/avimind_banner.png" alt="AviMind Banner" width="100%">
</p>

# 🧠 AviMind

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)
![PyPI](https://img.shields.io/pypi/v/avimind)

> **The open-source memory layer that gives AI agents long-term memory through semantic search, hybrid retrieval, intelligent ranking, and automatic deduplication.**

AviMind is an open-source persistent memory engine for AI agents and LLM-powered applications. It enables applications to remember user preferences, business context, conversations, and long-term knowledge across sessions.

Unlike traditional chat history, AviMind combines **semantic search**, **hybrid ranking**, **keyword awareness**, and **memory importance scoring** to retrieve the most relevant context for your AI applications.

# 📦 Install

```bash
pip install avimind
```

Then initialize the client:

```python
from avimind import AviMind

client = AviMind("http://localhost:8000")
```

---

# ✨ Features

* ✅ Persistent long-term memory
* ✅ Semantic search with embeddings
* ✅ Hybrid retrieval (semantic + keyword ranking)
* ✅ Automatic duplicate detection
* ✅ Memory importance scoring
* ✅ Intelligent context retrieval
* ✅ FastAPI REST APIs
* ✅ SQLite backend (zero configuration)
* ✅ Docker support
* ✅ Python SDK
* 🚧 PostgreSQL support (planned)
* 🚧 pgvector integration (planned)
* 🚧 Redis session memory (planned)


---

# 💡 Why AviMind?

Most AI agents forget everything after a conversation ends.

AviMind acts as a reusable memory layer that enables applications to remember:

* User preferences
* Business context
* Long-term facts
* Agent decisions
* Tool outputs
* Organizational knowledge
* Previous conversations

Instead of relying solely on exact keyword matching, AviMind uses embeddings and hybrid retrieval techniques to surface the most relevant memories automatically.

---

# 🚀 Example Use Cases

* AI chatbots with persistent memory
* Enterprise AI copilots
* Agentic workflows
* Customer support assistants
* Personal AI assistants
* Research assistants
* Knowledge management platforms
* LLM applications requiring long-term context

---

# ⚡ Quick Start

## Clone the repository

```bash
git clone https://github.com/avinashmhto/avimind.git

cd avimind
```

## Create a virtual environment

```bash
python -m venv .venv
```

### Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run AviMind Locally

```bash
uvicorn avimind_server.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 🐳 Run with Docker

Build and start AviMind:

```bash
docker compose up --build
```

Once the container is running, open:

```text
http://localhost:8000/docs
```

To stop the service:

```bash
docker compose down
```

AviMind uses SQLite by default and stores its database in the local `data/` directory, so no external database is required to get started.

---

# 🐍 Python SDK

AviMind ships with a lightweight Python SDK that makes integration straightforward.

## Create a client

```python
from avimind import AviMind

client = AviMind("http://localhost:8000")
Store a memory
client.remember(
    user_id="avinash",
    agent_id="sdk-agent",
    session_id="chat-001",
    memory_type="profile_memory",
    content="User prefers AWS Singapore region.",
    tags=["aws", "preference"],
    importance=0.9,
)
Search memories
results = client.search(
    user_id="avinash",
    query="Which cloud region does the user prefer?"
)

print(results)
Retrieve context
context = client.context(
    user_id="avinash",
    query="Which cloud region does the user prefer?"
)

print(context)
Check server health
status = client.health()

print(status)
Delete a memory
client.delete("memory-id")

The SDK currently supports:

health()
remember()
search()
context()
delete()

---


# 📝 Example

## Store a Memory

```json
{
  "user_id": "avinash",
  "agent_id": "goal-agent",
  "session_id": "goal-001",
  "memory_type": "goal_memory",
  "content": "User is building AviMind as an open-source persistent memory engine for AI agents.",
  "source": "manual",
  "created_by": "human",
  "tags": [
    "startup",
    "avimind",
    "opensource"
  ],
  "importance": 1.0
}
```

## Retrieve Context

**Query:**

```text
What startup is the user building?
```

**Response:**

```json
{
  "context": [
    "User is building AviMind as an open-source persistent memory engine for AI agents."
  ]
}
```

AviMind retrieves relevant memories using semantic understanding and hybrid ranking, even when the query wording differs from the original stored text.


---

# 🏗️ Core Capabilities

| Capability              | Status     |
| ----------------------- | ---------- |
| Persistent Memory       | ✅          |
| Semantic Search         | ✅          |
| Hybrid Retrieval        | ✅          |
| Automatic Deduplication | ✅          |
| Memory Ranking          | ✅          |
| Context Retrieval       | ✅          |
| FastAPI REST API        | ✅          |
| SQLite Backend          | ✅          |
| Docker Support          | ✅          |
| Python SDK              | ✅          | 
| PostgreSQL Backend      | 🚧 Planned |
| pgvector Integration    | 🚧 Planned |
| Redis Session Memory    | 🚧 Planned |

---

# 🚧 Current Status

**Version:** `v0.4`

Implemented:

* Persistent memory storage
* Semantic search
* Hybrid retrieval (semantic + keyword ranking)
* Automatic duplicate detection
* Memory importance scoring
* Context retrieval APIs
* SQLite backend
* Docker support
* REST APIs with Swagger documentation

---

# 🛣️ Roadmap

## v0.4

* Python SDK 
* Memory update APIs 
* Memory listing APIs 
* Memory expiration policies

with:

## v0.5

* Memory update APIs
* Memory listing APIs
* Memory expiration policies
* Publish SDK to PyPI
* Authentication support for SDK

## v1.0

* PostgreSQL backend
* pgvector integration
* Redis session memory
* Multi-tenant support
* OpenAI integration
* Ollama integration
* LangGraph integration
* MCP compatibility
* Cloud deployment guides

---

# 🤝 Contributing

Contributions, ideas, feature requests, and pull requests are welcome.

If AviMind helps your AI applications become smarter and more context-aware, please consider giving the project a ⭐ on GitHub.

---

# 📄 License

Released under the MIT License.

---

# 👨‍💻 Author

**Avinash Mahto**

Building practical infrastructure for AI agents, enterprise GenAI, cloud-native platforms, and intelligent memory systems.
