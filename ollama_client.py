import requests
import re
from config import OLLAMA_HOST, OLLAMA_MODEL, MYSQL_DATABASE
 
 
def extract_sql(text: str) -> str:
    """Extract SQL from Ollama's response."""
    # Try to find SQL in code blocks first
    code_block = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if code_block:
        return code_block.group(1).strip()
 
    # Look for SELECT, INSERT, UPDATE, DELETE, CREATE statements
    sql_match = re.search(
        r"(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|WITH)\s.+",
        text,
        re.DOTALL | re.IGNORECASE
    )
    if sql_match:
        return sql_match.group(0).strip()
 
    return text.strip()
 
 
def ask_ollama(user_question: str, schema: str, chat_history: list) -> dict:
    """
    Send user question + schema to Ollama and get SQL + explanation back.
    Returns dict with 'sql' and 'explanation'.
    """
 
    # ✅ Fix: Limit schema to 1500 chars to avoid timeout
    schema_short = schema[:1500] if len(schema) > 1500 else schema
 
    system_prompt = f"""You are a MySQL SQL assistant.
MySQL database schema:
 
{schema_short}
 
STRICT RULES:
- ALWAYS return a SQL query.
- When user says "show table X", write: SELECT * FROM X
- When user says "show all tables", write: SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{MYSQL_DATABASE}'
- Use MySQL syntax (LIMIT not ROWNUM).
- Do NOT add semicolon at end of SQL.
- Reply in this EXACT format only:
 
SQL:
```sql
<your SQL here>
```
 
EXPLANATION:
<one line explanation>
"""
 
    # Build messages with history (limit to last 4 messages only)
    messages = [{"role": "system", "content": system_prompt}]
 
    for entry in chat_history[-4:]:  # ✅ Reduced from 6 to 4
        messages.append({"role": entry["role"], "content": entry["content"]})
 
    messages.append({"role": "user", "content": user_question})
 
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "options": {
                    "num_predict": 300,   # ✅ Limit response length
                    "temperature": 0.1    # ✅ More focused/deterministic
                }
            },
            timeout=600
        )
        response.raise_for_status()
        raw = response.json()["message"]["content"]
 
        # Parse SQL and explanation
        sql = ""
        explanation = ""
 
        sql_match = re.search(r"SQL:\s*```(?:sql)?\s*(.*?)```", raw, re.DOTALL | re.IGNORECASE)
        if sql_match:
            # ✅ Strip semicolon from extracted SQL
            sql = sql_match.group(1).strip().rstrip(";").strip()
 
        exp_match = re.search(r"EXPLANATION:\s*(.*?)(?:$)", raw, re.DOTALL | re.IGNORECASE)
        if exp_match:
            explanation = exp_match.group(1).strip()
        else:
            explanation = raw if not sql else "Query generated successfully."
 
        return {"sql": sql, "explanation": explanation, "raw": raw}
 
    except requests.exceptions.ConnectionError:
        return {
            "sql": "",
            "explanation": "",
            "error": "❌ Cannot connect to Ollama. Make sure Ollama is running on your machine."
        }
    except Exception as e:
        return {"sql": "", "explanation": "", "error": f"❌ Ollama error: {str(e)}"}
