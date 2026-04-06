# ─────────────────────────────────────────────
#  ORACLE DATABASE CONFIGURATION
# ─────────────────────────────────────────────

ORACLE_USER     = "hr"       # e.g. "SCOTT"
ORACLE_PASSWORD = "hr"       # e.g. "tiger"
ORACLE_DSN      = "localhost:1521/xe" # host:port/service_name
# Examples:
#   "localhost:1521/ORCL"
#   "192.168.1.10:1521/XEPDB1"
#   "myserver:1521/FREEPDB1"


# ─────────────────────────────────────────────
#  OLLAMA CONFIGURATION
# ─────────────────────────────────────────────

OLLAMA_HOST  = "http://localhost:11434"  # Ollama default
OLLAMA_MODEL = "llama3.2:1b"                # Model pulled in Ollama


# ─────────────────────────────────────────────
#  APP CONFIGURATION
# ─────────────────────────────────────────────

APP_HOST = "0.0.0.0"
APP_PORT = 8000
