# 🚀 Railway Deployment Guide

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app)
2. **GitHub Account**: Your project should be on GitHub
3. **MySQL Database**: Must be accessible from Railway (cloud instance, not localhost)
4. **Ollama Service**: Must be accessible from Railway

---

## Step 1: Prepare for Deployment

### Update config.py with Environment Variables

Update [config.py](config.py) to read from environment variables instead of hardcoded values:

```python
import os

# ─────────────────────────────────────────────
#  MYSQL DATABASE CONFIGURATION
# ─────────────────────────────────────────────

MYSQL_USER     = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "ITNBUfHUjIAfoVmZgmeSJVEJHvmYVRvD")
MYSQL_HOST     = os.getenv("MYSQL_HOST", "shuttle.proxy.rlwy.net")
MYSQL_PORT     = int(os.getenv("MYSQL_PORT",45374 ))
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "railway")


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

### Update main.py for MySQL

No Oracle client initialization is needed for MySQL. Just ensure `main.py` imports the `db` helper and starts the FastAPI app normally.

---

## Step 2: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit for Railway deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/mysql-ai-chat.git
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
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=your_mysql_host
MYSQL_PORT=3306
MYSQL_DATABASE=your_mysql_database
OLLAMA_HOST=http://your_ollama_service:11434
OLLAMA_MODEL=llama3.2:1b
```

**Important Notes:**
- ✅ Use **cloud/network** MySQL instance (not localhost)
- ✅ Use **cloud/accessible** Ollama instance (not your local machine)
- ❌ Don't use localhost, 127.0.0.1, or private IPs unless Railway can reach them

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
| **MySQL connection fails** | Verify MySQL is accessible from internet; check host, port, and credentials |
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
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
