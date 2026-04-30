import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import uvicorn
from contextlib import asynccontextmanager

from db import get_schema_info, run_query
from ollama_client import ask_ollama
from config import APP_HOST, APP_PORT

# ── In-memory schema cache ──
_schema_cache = {"text": "", "tables": []}

# ── In-memory chat history ──
chat_history: List[dict] = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load schema on startup."""
    try:
        schema_text, tables = get_schema_info()
        _schema_cache["text"] = schema_text
        _schema_cache["tables"] = tables
        print(f"✅ Schema loaded: {len(tables)} tables found.")
    except Exception as e:
        print(f"⚠️  Could not load schema on startup: {e}")
        print("   Make sure MySQL DB is running and config.py is set correctly.")
    yield

app = FastAPI(title="Oracle AI Chat", version="1.0.0", lifespan=lifespan)


# ══════════════════════════════════════════════
#  MODELS
# ══════════════════════════════════════════════

class ChatRequest(BaseModel):
    question: str

class ExecuteRequest(BaseModel):
    sql: str


# ══════════════════════════════════════════════

#  ROUTES
# ══════════════════════════════════════════════

@app.get("/")
async def root():
    return FileResponse("static/index.html")


@app.get("/api/schema")
async def get_schema():
    """Return the current database schema."""
    if not _schema_cache["text"]:
        try:
            schema_text, tables = get_schema_info()
            _schema_cache["text"] = schema_text
            _schema_cache["tables"] = tables
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"DB Error: {str(e)}")
    return {
        "schema": _schema_cache["text"],
        "tables": _schema_cache["tables"],
        "table_count": len(_schema_cache["tables"])
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """
    Main chat endpoint:
    1. Send question + schema to Ollama → get SQL
    2. Execute SQL on MySQL
    3. Return results
    """
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    schema = _schema_cache["text"]
    if not schema:
        # Try to reload
        try:
            schema, tables = get_schema_info()
            _schema_cache["text"] = schema
            _schema_cache["tables"] = tables
        except Exception as e:
            return {
                "question": question,
                "error": f"Cannot connect to MySQL DB: {str(e)}",
                "sql": "",
                "explanation": "",
                "results": []
            }

    # Ask Ollama
    llm_response = ask_ollama(question, schema, chat_history)

    if "error" in llm_response:
        return {
            "question": question,
            "error": llm_response["error"],
            "sql": "",
            "explanation": "",
            "results": []
        }

    sql = llm_response.get("sql", "")
    explanation = llm_response.get("explanation", "")
    results = []

    # Execute SQL if we got one
    if sql:
        results = run_query(sql)

    # Update chat history
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": llm_response.get("raw", "")})

    # Keep history to last 20 messages
    if len(chat_history) > 20:
        chat_history[:] = chat_history[-20:]

    return {
        "question": question,
        "sql": sql,
        "explanation": explanation,
        "results": results,
        "error": ""
    }


@app.post("/api/execute")
async def execute_sql(req: ExecuteRequest):
    """Directly execute a SQL query."""
    if not req.sql.strip():
        raise HTTPException(status_code=400, detail="SQL cannot be empty.")
    results = run_query(req.sql)
    return {"results": results}


@app.delete("/api/history")
async def clear_history():
    """Clear chat history."""
    chat_history.clear()
    return {"message": "Chat history cleared."}


@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "llama3", "db": "mysql"}


# ══════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════

if __name__ == "__main__":
    uvicorn.run("main:app", host=APP_HOST, port=APP_PORT, reload=True)