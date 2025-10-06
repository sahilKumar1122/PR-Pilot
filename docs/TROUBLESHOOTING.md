# Troubleshooting Guide

Common issues and solutions for PR Pilot.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Connection Issues](#connection-issues)
- [GitHub Integration Issues](#github-integration-issues)
- [AI/HuggingFace Issues](#aihuggingface-issues)
- [Docker Issues](#docker-issues)
- [Performance Issues](#performance-issues)
- [Debugging Tips](#debugging-tips)

---

## Installation Issues

### Python Version Errors

**Problem:** `psycopg2-binary` fails to install on Python 3.13

**Solution:**
```bash
# Use psycopg instead (Python 3.13 compatible)
pip install psycopg[binary]>=3.2.0

# Already fixed in requirements.txt
```

**Problem:** `uvicorn` not found after installation

**Solution:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Or use full path
.\venv\Scripts\python.exe -m uvicorn main:app
```

### Dependency Conflicts

**Problem:** Version conflicts during `pip install`

**Solution:**
```bash
# Use fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Connection Issues

### Redis Connection Failed

**Problem:**
```
redis.exceptions.ConnectionError: Error 10061 connecting to localhost:6379
Connection refused
```

**Solution:**

**Docker:**
```bash
# Check Redis container is running
docker compose ps redis

# View Redis logs
docker compose logs redis

# Restart Redis
docker compose restart redis
```

**Manual:**
```bash
# Check if Redis is running
redis-cli ping
# Expected: PONG

# Start Redis (Linux)
sudo systemctl start redis

# Start Redis (macOS)
brew services start redis

# Check Redis port
netstat -an | grep 6379
```

**Environment Variable:**
```bash
# Check .env file
cat .env | grep REDIS_URL

# Should be:
REDIS_URL=redis://localhost:6379/0  # Local
REDIS_URL=redis://redis:6379/0      # Docker
```

### PostgreSQL Connection Failed

**Problem:**
```
psycopg.OperationalError: connection to server failed
FATAL: password authentication failed for user "prpilot"
```

**Solution:**

**Check Connection String:**
```bash
# .env file format
DATABASE_URL=postgresql://username:password@host:port/database

# Example (Docker):
DATABASE_URL=postgresql://prpilot:devpassword@postgres:5432/prpilot

# Example (Local):
DATABASE_URL=postgresql://prpilot:devpassword@localhost:5432/prpilot
```

**Docker Fix:**
```bash
# Recreate database with fresh data
docker compose down -v  # ⚠️ This deletes all data!
docker compose up -d

# Check PostgreSQL logs
docker compose logs postgres
```

**Local Fix:**
```bash
# Reset password
sudo -u postgres psql
postgres=# ALTER USER prpilot WITH PASSWORD 'your_password';
postgres=# \q

# Create database if missing
sudo -u postgres createdb prpilot
```

**IPv6 Issue (Windows):**
```python
# Use 127.0.0.1 instead of localhost
DATABASE_URL=postgresql://prpilot:password@127.0.0.1:5432/prpilot
```

---

## GitHub Integration Issues

### Webhook Not Triggering

**Problem:** PR opened, but no comment posted

**Checklist:**

1. **Verify webhook is configured:**
   - Go to GitHub repo → Settings → Webhooks
   - Should see your webhook URL
   - Check "Recent Deliveries" for errors

2. **Check webhook endpoint is accessible:**
   ```bash
   curl http://your-domain.com/webhooks/github
   ```
   If local testing, use ngrok:
   ```bash
   # Install ngrok
   brew install ngrok  # macOS
   # or download from ngrok.com

   # Expose local port
   ngrok http 8000
   
   # Use ngrok URL in GitHub webhook settings
   # e.g., https://abc123.ngrok.io/webhooks/github
   ```

3. **Verify webhook secret matches:**
   ```bash
   # .env file
   echo $GITHUB_WEBHOOK_SECRET
   
   # GitHub webhook settings
   # Should be the same!
   ```

4. **Check backend logs:**
   ```bash
   docker compose logs -f backend
   # Look for:
   # 📥 Received PR event: owner/repo#123
   ```

### GitHub API Rate Limit

**Problem:**
```
github.GithubException.RateLimitExceededException: 403
API rate limit exceeded
```

**Solution:**

```bash
# Check your rate limit
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# If exceeded, wait or:
# 1. Use a different token
# 2. Request higher rate limit from GitHub
# 3. Implement caching for API calls
```

**For authenticated requests:** 5,000/hour
**For unauthenticated:** 60/hour (never use this!)

### Invalid GitHub Token

**Problem:**
```
github.GithubException.BadCredentialsException: 401
Bad credentials
```

**Solutions:**

1. **Token expired or revoked:**
   - Generate new token: https://github.com/settings/tokens
   - Update `.env` with new token

2. **Wrong token format:**
   ```bash
   # Should start with ghp_
   GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

3. **Insufficient permissions:**
   - Token needs `repo` scope
   - For public repos only: `public_repo` scope

4. **Test token manually:**
   ```bash
   curl -H "Authorization: token $GITHUB_TOKEN" \
     https://api.github.com/user
   ```

### Comment Not Posted

**Problem:** Analysis completes but no comment appears on PR

**Check:**

1. **Worker logs:**
   ```bash
   docker compose logs -f worker
   # Look for errors after "📤 Posting comment to GitHub..."
   ```

2. **Token permissions:**
   - Needs `repo` scope or `public_repo` for public repos
   - For organization repos: Enable "Configure SSO" on token

3. **Repository permissions:**
   - Bot user needs write access to repository
   - Check repo settings → Collaborators

---

## AI/HuggingFace Issues

### SSL Certificate Error

**Problem:**
```
SSLCertVerificationError: certificate verify failed: 
self-signed certificate in certificate chain
```

**Cause:** Corporate network with SSL inspection

**Solution (Development only):**

Already fixed in code with monkey patch in `huggingface_client.py`.

For production, add corporate CA certificate:
```bash
# Add CA cert to requests
export REQUESTS_CA_BUNDLE=/path/to/corporate-ca.crt
```

### HuggingFace Model Timeout

**Problem:**
```
504 Server Error: Gateway Time-out
```

**Cause:** Free tier models may be slow or "cold start"

**Solution:**

Already handled with fallbacks! But you can:

1. **Use HuggingFace Pro:**
   - Faster inference
   - No cold starts
   - Higher rate limits

2. **Self-host models:**
   ```python
   # Use local transformers instead
   from transformers import pipeline
   
   summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
   ```

3. **Use alternative models:**
   - Current: `facebook/bart-large-cnn`, `sshleifer/distilbart-cnn-12-6`
   - Fallback: Keyword extraction (no AI needed)

### Invalid HuggingFace API Key

**Problem:**
```
401 Client Error: Unauthorized
```

**Solution:**

```bash
# Check .env
cat .env | grep HF_API_KEY

# Generate new key: https://huggingface.co/settings/tokens
# Update .env
HF_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Restart services
docker compose restart
```

### Unexpected AI Response Format

**Problem:**
```
AttributeError: 'str' object has no attribute 'summary_text'
```

**Solution:**

Already fixed with robust response parsing in `huggingface_client.py`!

If you see this error in newer versions:

```python
# Check response type
print(f"Response type: {type(result)}")
print(f"Response content: {result}")

# Add more type checks in huggingface_client.py
```

---

## Docker Issues

### Docker Desktop Not Running

**Problem:**
```
error during connect: Get "http://.../v1.51/...": 
The system cannot find the file specified
```

**Solution:**

```bash
# Windows: Start Docker Desktop from Start menu
# Mac: Start Docker Desktop from Applications

# Verify Docker is running
docker ps
```

### Port Already in Use

**Problem:**
```
Error: Bind for 0.0.0.0:8000 failed: port is already allocated
```

**Solution:**

```bash
# Find process using port
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Or change port in docker-compose.yml:
# ports:
#   - "8001:8000"  # Use 8001 instead
```

### Docker Compose Version

**Problem:**
```bash
docker-compose: command not found
```

**Solution:**

```bash
# Docker Compose V2 (current):
docker compose up -d

# Docker Compose V1 (legacy):
docker-compose up -d

# Install V2:
apt-get install docker-compose-plugin
```

### Container Keeps Restarting

**Problem:** Container starts then immediately stops

**Solution:**

```bash
# View logs
docker compose logs backend
docker compose logs worker

# Common causes:
# 1. Missing environment variables
# 2. Connection to Redis/PostgreSQL failed
# 3. Syntax error in code
# 4. Missing dependencies

# Debug by running manually:
docker compose run backend bash
# Then inside container:
python -m uvicorn main:app
```

### Docker Build Fails

**Problem:** `docker compose build` fails

**Solution:**

```bash
# Clear build cache
docker builder prune -a

# Rebuild from scratch
docker compose build --no-cache

# Check Docker disk space
docker system df

# Clean up if needed
docker system prune -a
```

---

## Performance Issues

### Slow PR Analysis

**Problem:** Takes > 2 minutes to analyze PR

**Causes & Solutions:**

1. **Large PRs:**
   - 50+ files changed
   - 1000+ lines changed
   - **Solution:** Implement PR size limits or split analysis

2. **HuggingFace timeout:**
   - Free tier is slow
   - **Solution:** Upgrade to HuggingFace Pro or self-host models

3. **Network latency:**
   - Slow connection to GitHub API
   - **Solution:** Deploy closer to GitHub servers (US/EU regions)

4. **Worker overload:**
   - Too many concurrent analyses
   - **Solution:** Scale workers or increase concurrency:
     ```bash
     docker compose up -d --scale worker=3
     # or
     celery -A tasks worker --concurrency=4
     ```

### High Memory Usage

**Problem:** Worker uses > 2GB RAM

**Cause:** AI models loaded in memory

**Solutions:**

1. **Limit worker concurrency:**
   ```bash
   # Only process 1 PR at a time
   celery -A tasks worker --concurrency=1
   ```

2. **Use smaller models:**
   ```python
   # In huggingface_client.py
   # Use distilbart instead of bart-large
   model = "sshleifer/distilbart-cnn-12-6"
   ```

3. **Add more RAM:**
   - Minimum: 2GB
   - Recommended: 4GB per worker

### Redis/PostgreSQL Connection Pool Exhausted

**Problem:**
```
redis.exceptions.ConnectionError: Too many connections
```

**Solution:**

```python
# Increase Redis max connections
# redis.conf:
maxclients 10000

# Or configure Celery connection pool:
# worker/tasks.py
celery_app = Celery(
    "pr-pilot",
    broker=redis_url,
    broker_pool_limit=10  # Limit connections
)
```

---

## Debugging Tips

### Enable Debug Logging

```bash
# .env
LOG_LEVEL=DEBUG

# Restart services
docker compose restart
```

### Check Service Health

```bash
# Backend
curl http://localhost:8000/

# Redis
redis-cli ping

# PostgreSQL
docker compose exec postgres psql -U prpilot -c "SELECT 1;"

# Celery workers
docker compose exec worker celery -A tasks inspect active
```

### View All Logs

```bash
# Docker: All services
docker compose logs -f

# Docker: Specific service
docker compose logs -f backend
docker compose logs -f worker

# Follow logs with grep
docker compose logs -f | grep ERROR
docker compose logs -f | grep "PR event"
```

### Test Components Independently

**Test Backend Only:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
# Test: curl http://localhost:8000/
```

**Test Worker Only:**
```bash
cd worker
source venv/bin/activate
celery -A tasks worker --loglevel=debug
# Enqueue test task: python tests/test_webhook.py
```

**Test AI Analysis:**
```bash
cd worker
source venv/bin/activate
python -c "
from integrations.huggingface_client import HuggingFaceClient
client = HuggingFaceClient()
print(client.summarize('This is a test PR that adds new features'))
"
```

### Network Debugging

```bash
# Test external connectivity
docker compose exec backend curl https://api.github.com
docker compose exec worker curl https://huggingface.co

# Test internal connectivity
docker compose exec backend ping redis
docker compose exec worker ping postgres

# Check DNS resolution
docker compose exec backend nslookup github.com
```

### Database Debugging

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U prpilot

# List tables
\dt

# Query PR analyses (when implemented)
SELECT * FROM pr_analyses LIMIT 10;

# Check connections
SELECT count(*) FROM pg_stat_activity;
```

---

## Common Error Messages

### `ModuleNotFoundError: No module named 'worker'`

**Fix:** Already fixed in v0.1.0! Backend uses `celery_app.send_task()` instead of importing worker tasks.

### `UnicodeEncodeError` (Windows)

**Fix:** Already fixed! Removed emojis from Windows output.

### `CERTIFICATE_VERIFY_FAILED`

**Fix:** Already fixed! Disabled SSL verification for corporate networks (dev only).

### `process completed with exit code 1`

**Cause:** Generic error in CI/CD or Docker

**Debug:**
```bash
# Check GitHub Actions logs
# Or run locally:
docker compose logs -f
```

---

## Still Having Issues?

### Before Asking for Help

1. **Check logs:**
   ```bash
   docker compose logs -f > logs.txt
   ```

2. **Test connections:**
   ```bash
   python tests/test_connections.py
   ```

3. **Verify environment:**
   ```bash
   cat .env  # (redact secrets!)
   docker compose config  # Validate compose file
   ```

4. **System info:**
   ```bash
   docker --version
   python --version
   docker compose version
   ```

### Get Help

1. **Search existing issues:**
   https://github.com/sahilKumar1122/PR-Pilot/issues

2. **GitHub Discussions:**
   https://github.com/sahilKumar1122/PR-Pilot/discussions

3. **Create new issue:**
   - Include error message
   - Include relevant logs
   - Include system info
   - Steps to reproduce

---

## Contributing Fixes

Found a bug? Know the fix? Please contribute!

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.
