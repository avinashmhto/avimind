# 🧠 AviMind

> **🧠 Give your AI agents long-term memory with semantic search, intelligent retrieval, and automatic deduplication.**

AviMind is an open-source memory layer that enables AI agents to remember information across conversations using semantic search, intelligent ranking, and automatic deduplication.

Unlike simple chat history, AviMind stores structured long-term memory that can be retrieved based on meaning rather than exact keywords.

---

## ✨ Features

- 🔍 Semantic memory retrieval using embeddings
- 🧠 Persistent long-term memory storage
- 🚫 Automatic duplicate detection
- ⭐ Memory importance scoring and ranking
- ⚡ FastAPI REST APIs
- 💾 SQLite support out of the box
- 🔌 Framework agnostic (works with any LLM or AI agent)
- 🏗️ Designed for future PostgreSQL, pgvector, and Redis support

---

## 🚀 Why AviMind?

Most LLMs forget everything when a conversation ends.

AviMind gives your AI applications a persistent memory layer so they can remember:

- User preferences
- Past decisions
- Business context
- Agent outputs
- Important facts
- Tool results

This enables more personalized and context-aware AI experiences.

---

## 🏛️ High-Level Architecture

```text
                 +----------------------+
                 |   AI Agent / LLM     |
                 +----------+-----------+
                            |
                            |
                     REST API Calls
                            |
                            v
                +------------------------+
                |       AviMind API      |
                |        (FastAPI)       |
                +-----------+------------+
                            |
            +---------------+----------------+
            |                                |
            | Semantic Embeddings            |
            | Duplicate Detection            |
            | Memory Ranking                 |
            +---------------+----------------+
                            |
                            v
                  +--------------------+
                  |    SQLite (v0.2)   |
                  |  Persistent Memory |
                  +--------------------+

                (PostgreSQL / pgvector /
                 Redis support planned)
```

---

## 📦 Installation

```bash
git clone <repository-url>

cd avimind

python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows Git Bash
source .venv/Scripts/activate

pip install -r requirements.txt

uvicorn avimind_server.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 📝 Example: Store Memory

`POST /memory`

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

---

## 🔎 Example: Semantic Search

```
GET /memory/search?user_id=avinash&query=Which cloud region does the user prefer?
```

AviMind retrieves the relevant memory even when the wording differs from the original stored text.

---

## 🎯 Current Capabilities

| Feature | Status |
|----------|--------|
| Persistent Memory | ✅ |
| Semantic Search | ✅ |
| Memory Scoring | ✅ |
| Automatic Deduplication | ✅ |
| FastAPI REST APIs | ✅ |
| SQLite Backend | ✅ |
| PostgreSQL Backend | 🚧 Planned |
| pgvector Support | 🚧 Planned |
| Redis Session Memory | 🚧 Planned |
| Python SDK | 🚧 Planned |
| Docker Deployment | 🚧 Planned |

---

## 🗺️ Roadmap

### v0.2
- Semantic search
- Memory scoring
- Duplicate detection
- SQLite persistence

### v0.3
- Python SDK
- Docker support
- Memory listing APIs
- Memory update APIs

### v1.0
- PostgreSQL backend
- pgvector integration
- Redis session memory
- Multi-tenant support
- Production deployment guides

---

## 🤝 Contributing

Contributions, ideas, bug reports, and feature requests are welcome.

If you find AviMind useful, consider starring the repository and sharing your feedback.

---

## 📄 License

Released under the MIT License.

---

## 👨‍💻 Author

**Avinash Mahto**

Building practical infrastructure for AI agents, enterprise GenAI, and cloud-native platforms.