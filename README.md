<<<<<<< HEAD
# 🔥 MySQL AI Chat — Offline Database Assistant

Chat with your MySQL database in plain English.  
**100% offline** — powered by Ollama (llama3) + FastAPI.

---

## 🏗️ Architecture

```
User (Browser)
    │
    ▼
FastAPI (main.py)
    │
    ├──► Ollama llama3 ──► Generates SQL from natural language
    │
    └──► MySQL DB ──────► Executes SQL, returns results
```

---

## ✅ Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| Python | 3.9+ | `python --version` |
| MySQL DB | Any | Running locally or on network |
| Ollama | Latest | `ollama --version` |
| llama3 model | — | `ollama pull llama3` |

---

## ⚙️ Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your MySQL connection

Edit `config.py`:

```python
MYSQL_USER     = "your_username"
MYSQL_PASSWORD = "your_password"
MYSQL_HOST     = "localhost"
MYSQL_PORT     = 3306
MYSQL_DATABASE = "your_database"
```

### 3. Make sure Ollama is running

```bash
# Start Ollama (if not already running)
ollama serve

# Pull llama3 (if not already pulled)
ollama pull llama3
```

### 4. Run the app

```bash
python main.py
```

Then open your browser at:  
👉 **http://localhost:8000**

---

## 💬 How it works

1. You type a question in plain English, e.g.:  
   *"Show me the top 5 customers by total order amount"*

2. FastAPI sends the question + your full DB schema to **Ollama llama3**

3. llama3 generates an **MySQL SQL query**

4. FastAPI **executes the SQL** on your MySQL database

5. Results are displayed as a **table** in the chat UI

---

## 🗂️ Project Structure

```
mysql-ai-chat/
├── main.py           # FastAPI app (routes, startup)
├── db.py             # MySQL DB connection & queries
├── ollama_client.py  # Ollama API integration
├── config.py         # ⚠️ Edit this with your settings
├── requirements.txt  # Python dependencies
├── static/
│   └── index.html    # Chat UI (dark theme)
└── README.md
```

---

## 🔧 Troubleshooting

| Issue | Fix |
|-------|-----|
| `Cannot connect to MySQL` | Verify MySQL is running and config.py is set correctly |
| `Cannot connect to Ollama` | Run `ollama serve` first |
| `Access denied` | Check MySQL credentials and permissions |
| Schema loads but queries fail | Make sure user has SELECT privilege on tables |

---

## 🎨 Features

- 🌑 Dark-themed chat interface
- 🧠 Natural language → SQL via llama3
- 📊 Results displayed as interactive tables
- 📋 Copy SQL button
- 📁 Schema viewer in sidebar
- 🔄 Multi-turn conversation memory (last 3 exchanges)
- 🗑️ Clear chat history button
- ⚡ 100% offline — no internet required

