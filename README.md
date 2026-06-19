<p align="center">
  <img src="assets/avimind_banner.png" alt="AviMind Banner" width="100%">
</p>

# 🧠 AviMind

> **The open-source memory layer that gives AI agents long-term memory through semantic search, intelligent retrieval, and automatic deduplication.**

AviMind is an open-source persistent memory engine designed for AI agents and LLM-powered applications. It enables applications to remember user preferences, past interactions, business context, and important knowledge across sessions.

Unlike traditional chat history, AviMind retrieves memories based on **meaning**, not just exact keyword matches, helping AI systems deliver smarter and more personalized responses.

---

# ✨ Key Features

* ✅ Persistent long-term memory
* ✅ Semantic search using vector embeddings
* ✅ Automatic duplicate detection
* ✅ Memory importance scoring and ranking
* ✅ Intelligent context retrieval
* ✅ FastAPI REST APIs
* ✅ SQLite backend (zero configuration)
* 🚧 PostgreSQL support (planned)
* 🚧 pgvector integration (planned)
* 🚧 Redis session memory (planned)
* 🚧 Python SDK (planned)
* 🚧 Docker support (planned)

---

# 💡 Why AviMind?

Most AI agents lose context once a conversation ends.

AviMind provides a reusable memory layer that allows applications to remember:

* User preferences
* Business context
* Prior conversations
* Agent decisions
* Tool outputs
* Long-term facts
* Organizational knowledge

Instead of relying on exact keyword matching, AviMind uses semantic understanding to retrieve the most relevant memories.

---

# 🚀 Example Use Cases

* AI chatbots with persistent user memory
* Enterprise AI copilots
* Customer support assistants
* Agentic workflows
* Research assistants
* Personal AI assistants
* Knowledge management systems
* LLM applications requiring long-term context

---

# ⚡ Quick Start

## Clone the repository

```bash
git clone https://gitlab.com/avinashmahto/avimind.git

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

## Run AviMind

```bash
uvicorn avimind_server.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

# 📝 Example Memory

```json
{
  "user_id": "avinash",
  "agent_id": "demo-agent",
  "session_id": "chat-001",
  "memory_type": "profile_memory",
  "content": "User prefers AWS Singapore region and simple human language.",
  "source": "manual",
  "created_by": "human",
  "tags": [
    "aws",
    "singapore",
    "preference"
  ],
  "importance": 0.9
}
```

Example semantic query:

```
Which cloud region does the user prefer?
```

AviMind can retrieve the correct memory even when the query wording differs from the original stored text.

---

# 🏗️ Core Capabilities

| Capability              | Status     |
| ----------------------- | ---------- |
| Persistent Memory       | ✅          |
| Semantic Search         | ✅          |
| Automatic Deduplication | ✅          |
| Memory Ranking          | ✅          |
| Context Retrieval       | ✅          |
| FastAPI REST API        | ✅          |
| SQLite Backend          | ✅          |
| PostgreSQL Backend      | 🚧 Planned |
| pgvector Support        | 🚧 Planned |
| Redis Session Memory    | 🚧 Planned |
| Python SDK              | 🚧 Planned |
| Docker Support          | 🚧 Planned |

---

# 🚧 Project Status

AviMind is under active development.

**Current release:** v0.2

Implemented today:

* Semantic memory retrieval
* Embedding-based search
* Automatic duplicate detection
* Memory scoring
* SQLite persistence
* REST APIs

Upcoming releases will focus on production deployments, SDKs, Docker, PostgreSQL, Redis, and framework integrations.

---

# 🛣️ Roadmap

## v0.3

* Docker support
* Python SDK
* Memory listing APIs
* Memory update APIs

## v1.0

* PostgreSQL backend
* pgvector integration
* Redis session memory
* Multi-tenant architecture
* Production deployment guides
* OpenAI integration examples
* Ollama integration examples
* LangGraph integration examples
* MCP compatibility

---

# 🤝 Contributing

Contributions, feature requests, bug reports, and ideas are always welcome.

If AviMind helps your AI applications become more context-aware, consider starring the repository and sharing your feedback.

---

# 📄 License

Released under the MIT License.

---

# 👨‍💻 Author

**Avinash Mahto**

Building practical infrastructure for AI agents, enterprise GenAI, and cloud-native platforms.
