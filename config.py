import os

# ─────────────────────────────────────────────
#  ORACLE DATABASE CONFIGURATION
# ─────────────────────────────────────────────

ORACLE_USER     = os.getenv("ORACLE_USER", "hr")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "hr")
ORACLE_DSN      = os.getenv("ORACLE_DSN", "localhost:1521/xe")
ORACLE_INSTANT_CLIENT = os.getenv("ORACLE_INSTANT_CLIENT", None)
# Examples:
#   "localhost:1521/ORCL"
#   "192.168.1.10:1521/XEPDB1"
#   "myserver:1521/FREEPDB1"


# ─────────────────────────────────────────────
#  OLLAMA CONFIGURATION
# ─────────────────────────────────────────────

OLLAMA_HOST  = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


# ─────────────────────────────────────────────
#  APP CONFIGURATION
# ─────────────────────────────────────────────

APP_HOST = "0.0.0.0"
APP_PORT = int(os.getenv("PORT", 8000))
