# 🚀 Railway Deployment Guide

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: Your project should be on GitHub
3. **Oracle Database**: Must be accessible from Railway (cloud instance, not localhost)
4. **Ollama Service**: Must be accessible from Railway

---

## Step 1: Prepare for Deployment

### Update config.py with Environment Variables

Update [config.py](config.py) to read from environment variables instead of hardcoded values:

```python
import os

# ─────────────────────────────────────────────
#  ORACLE DATABASE CONFIGURATION
# ─────────────────────────────────────────────

ORACLE_USER     = os.getenv("ORACLE_USER", "hr")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "hr")
ORACLE_DSN      = os.getenv("ORACLE_DSN", "localhost:1521/xe")
ORACLE_INSTANT_CLIENT = os.getenv("ORACLE_INSTANT_CLIENT", None)


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
```

### Update main.py for Oracle Instant Client

Modify the Oracle client initialization in [main.py](main.py):

```python
import oracledb
import os
from config import ORACLE_INSTANT_CLIENT

# Initialize Oracle Instant Client if path is provided
if ORACLE_INSTANT_CLIENT and os.path.exists(ORACLE_INSTANT_CLIENT):
    oracledb.init_oracle_client(ORACLE_INSTANT_CLIENT)
```

---

## Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit for Railway deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/oracle-ai-chat.git
git push -u origin main
```

---

## Step 3: Deploy on Railway

### Option A: Using Railway CLI (Recommended)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and Deploy**:
   ```bash
   railway init
   railway up
   ```

### Option B: Using Railway Dashboard

1. Go to [railway.app/dashboard](https://railway.app/dashboard)
2. Click **New Project**
3. Select **Deploy from GitHub**
4. Connect your GitHub repository
5. Railway will auto-detect Python and use the Procfile
6. Configure environment variables (see Step 4)
7. Deploy!

---

## Step 4: Configure Environment Variables

In Railway Dashboard, go to your project → **Variables** tab and add:

```
ORACLE_USER=your_oracle_user
ORACLE_PASSWORD=your_oracle_password
ORACLE_DSN=your_oracle_host:your_oracle_port/your_service_name
ORACLE_INSTANT_CLIENT=/path/to/oracle/client  # (if applicable)
OLLAMA_HOST=http://your_ollama_service:11434
OLLAMA_MODEL=llama3.2:1b
```

**Important Notes:**
- ✅ Use **cloud/network** Oracle instance (not localhost)
- ✅ Use **cloud/accessible** Ollama instance (not your local machine)
- ❌ Don't use localhost, 127.0.0.1, or private IPs

---

## Step 5: Verify Deployment

1. Go to Railway Dashboard → your project → **Deployments**
2. View logs to confirm the app started: `✅ Schema loaded: X tables found`
3. Click **Public URL** to access your app
4. Test the API: `https://your-app.railway.app/docs`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **Oracle connection fails** | Verify Oracle is accessible from internet; check DSN and credentials |
| **Ollama not found** | Ensure Ollama service is running on a public URL |
| **Port 8000 already in use** | Railway uses $PORT env var automatically; don't hardcode |
| **Import errors** | Verify all packages in requirements.txt are listed |

---

## Notes

- Railway provides a free tier suitable for testing
- Paid plans start at ~$5/month for production
- Static files in `/static` are served automatically
- Database connections stay encrypted in transit

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Oracle oracledb Python](https://python-oracledb.readthedocs.io/)
