<<<<<<< HEAD
# 🔥 Oracle AI Chat — Offline Database Assistant

Chat with your Oracle database in plain English.  
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
    └──► Oracle DB ──────► Executes SQL, returns results
```

---

## ✅ Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| Python | 3.9+ | `python --version` |
| Oracle DB | Any | Running locally or on network |
| Oracle Instant Client | 19c+ | Required by python-oracledb (thick mode) |
| Ollama | Latest | `ollama --version` |
| llama3 model | — | `ollama pull llama3` |

---

## ⚙️ Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure your Oracle connection

Edit `config.py`:

```python
ORACLE_USER     = "your_username"       # e.g. SCOTT
ORACLE_PASSWORD = "your_password"       # e.g. tiger
ORACLE_DSN      = "localhost:1521/ORCL" # host:port/service_name
```

Common DSN formats:
- `localhost:1521/ORCL`       — Oracle Database 19c
- `localhost:1521/XEPDB1`     — Oracle XE 21c
- `localhost:1521/FREEPDB1`   — Oracle Free 23c
- `192.168.1.10:1521/ORCL`   — Remote server

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

3. llama3 generates an **Oracle SQL query**

4. FastAPI **executes the SQL** on your Oracle database

5. Results are displayed as a **table** in the chat UI

---

## 🗂️ Project Structure

```
oracle-ai-chat/
├── main.py           # FastAPI app (routes, startup)
├── db.py             # Oracle DB connection & queries
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
| `DPI-1047: Cannot locate a 64-bit Oracle Client library` | Install Oracle Instant Client and set `LD_LIBRARY_PATH` |
| `Cannot connect to Ollama` | Run `ollama serve` first |
| `ORA-12541: TNS:no listener` | Oracle DB is not running or DSN is wrong |
| `ORA-01017: invalid username/password` | Check credentials in config.py |
| Schema loads but queries fail | Make sure user has SELECT privilege on tables |

---

## 🔐 Oracle Instant Client (if needed)

If you see the `DPI-1047` error, install Oracle Instant Client:

**Windows:**
1. Download from https://oracle.com/database/technologies/instant-client.html
2. Extract to `C:\oracle\instantclient_21_x`
3. Add to PATH

**Linux:**
```bash
sudo apt install libaio1
# Download instantclient-basiclite from Oracle
unzip instantclient-basiclite-*.zip -d /opt/oracle
export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_x:$LD_LIBRARY_PATH
```

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

