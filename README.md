<p align="center">
  <img src="assets/avimind_banner.png" alt="AviMind Banner" width="100%">
</p>

# 🧠 AviMind

> **Give your AI agents long-term memory with semantic search, intelligent retrieval, and automatic deduplication.**

Open-source persistent memory for AI agents and LLM applications with semantic search, intelligent ranking, and automatic deduplication.

---

## ✨ Why AviMind?

Most AI agents forget everything after a conversation ends.

AviMind provides a reusable memory layer that enables applications to remember:

- User preferences
- Business context
- Prior conversations
- Agent decisions
- Tool outputs
- Long-term facts

Unlike simple chat history, AviMind retrieves information based on **meaning**, not just exact keyword matches.

---

## 🚀 Features

- ✅ Persistent long-term memory
- ✅ Semantic search using embeddings
- ✅ Automatic duplicate detection
- ✅ Memory importance scoring
- ✅ Intelligent context retrieval
- ✅ FastAPI REST APIs
- ✅ SQLite backend (out of the box)
- 🚧 PostgreSQL support (planned)
- 🚧 pgvector integration (planned)
- 🚧 Redis session memory (planned)
- 🚧 Python SDK (planned)
- 🚧 Docker support (planned)

---

## ⚡ Quick Start

```bash
git clone https://gitlab.com/avinashmahto/avimind.git

cd avimind

python -m venv .venv

# Windows (Git Bash)
source .venv/Scripts/activate

# Linux / macOS
# source .venv/bin/activate

pip install -r requirements.txt

uvicorn avimind_server.main:app --reload

Open:

http://127.0.0.1:8000/docs

🏗️ Architecture
          AI Agent / LLM
                 │
                 │
          REST API Calls
                 │
                 ▼
        +-------------------+
        |     AviMind       |
        |  Memory Engine    |
        +-------------------+
          │      │      │
          │      │      │
     Semantic  Ranking  Deduplication
      Search
                 │
                 ▼
          SQLite Database

🛣️ Roadmap
🐳 Docker support
📦 Python SDK
🐘 PostgreSQL backend
🔎 pgvector integration
⚡ Redis session memory
🤖 LangGraph integration
🔌 MCP compatibility
☁️ Cloud deployment guides
📄 License

MIT License

👨‍💻 Author

Avinash Mahto


## One final suggestion

Your repository is already in good shape. I would make **one branding change**:

Change the subtitle from:

> **Persistent Memory Engine for AI Agents and LLM Applications**

to:

> **The open-source memory layer that gives AI agents long-term memory.**

It's shorter, more memorable, and immediately communicates the value proposition. After adding the banner image and this polished README, your project will look significantly more professional. 🚀