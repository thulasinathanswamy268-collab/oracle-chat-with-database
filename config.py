import os

# ─────────────────────────────────────────────
#  MYSQL DATABASE CONFIGURATION
# ─────────────────────────────────────────────

MYSQL_USER     = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ITNBUfHUjIAfoVmZgmeSJVEJHvmYVRvD")
MYSQL_HOST     = os.getenv("MYSQL_HOST", "shuttle.proxy.rlwy.net")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "railway")
# Example MySQL connection:
#   host=localhost, port=3306, database=mydb


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
