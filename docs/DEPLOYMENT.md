# Deployment Guide

This guide covers deploying PR Pilot to production environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Options](#deployment-options)
- [Docker Deployment (Recommended)](#docker-deployment-recommended)
- [Manual Deployment](#manual-deployment)
- [Cloud Platform Guides](#cloud-platform-guides)
- [Configuration](#configuration)
- [Monitoring & Logging](#monitoring--logging)
- [Scaling](#scaling)
- [Security](#security)

---

## Prerequisites

### Required Services

1. **Redis** (v7+)
   - Message broker for Celery
   - Can be self-hosted or use managed service (AWS ElastiCache, Redis Cloud, etc.)

2. **PostgreSQL** (v15+)
   - Database for storing PR metadata
   - Can be self-hosted or use managed service (AWS RDS, Supabase, etc.)

3. **Server/Compute**
   - Minimum: 1 CPU, 2GB RAM (for small projects)
   - Recommended: 2 CPU, 4GB RAM (for production)
   - Backend + Worker can run on same machine or separate

### Required Credentials

1. **GitHub Personal Access Token**
   - Scope: `repo` (full repository access)
   - Used to fetch PR diffs and post comments
   - Create at: https://github.com/settings/tokens

2. **HuggingFace API Key**
   - Free tier available
   - Used for AI model inference
   - Get at: https://huggingface.co/settings/tokens

3. **GitHub Webhook Secret**
   - Generate a random secret (32+ characters)
   - Used for webhook signature verification
   - Example: `openssl rand -hex 32`

---

## Deployment Options

### 1. Docker Deployment (Recommended)

✅ **Pros:**
- Consistent environment
- Easy setup and scaling
- Built-in service orchestration
- Works on any platform

❌ **Cons:**
- Requires Docker knowledge
- Higher resource usage

**Best for:** Most production deployments

### 2. Manual Deployment

✅ **Pros:**
- Lower resource usage
- More control
- No Docker required

❌ **Cons:**
- More setup steps
- Platform-specific
- Manual dependency management

**Best for:** Experienced ops teams, specific infrastructure requirements

### 3. Cloud Platforms

✅ **Pros:**
- Managed infrastructure
- Auto-scaling
- Built-in monitoring

❌ **Cons:**
- Higher costs
- Platform lock-in

**Best for:** Teams wanting minimal ops overhead

---

## Docker Deployment (Recommended)

### Step 1: Prepare Server

```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose V2
apt-get update
apt-get install docker-compose-plugin

# Verify
docker --version
docker compose version
```

### Step 2: Clone Repository

```bash
git clone https://github.com/sahilKumar1122/PR-Pilot.git
cd PR-Pilot
```

### Step 3: Configure Environment

```bash
# Copy example env file
cp env.example .env

# Edit with your values
nano .env
```

**Required Environment Variables:**

```bash
# GitHub Integration
GITHUB_TOKEN=ghp_your_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here

# HuggingFace AI
HF_API_KEY=hf_your_key_here

# Redis (use default for Docker Compose)
REDIS_URL=redis://redis:6379/0

# PostgreSQL (use default for Docker Compose)
DATABASE_URL=postgresql://prpilot:your_db_password@postgres:5432/prpilot
```

### Step 4: Start Services

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Check status
docker compose ps
```

### Step 5: Verify Deployment

```bash
# Test health endpoint
curl http://localhost:8000/

# Expected response:
# {"status":"healthy","service":"pr-pilot"}

# Check API docs
curl http://localhost:8000/docs
```

### Step 6: Configure GitHub Webhook

1. Go to your GitHub repository
2. Settings → Webhooks → Add webhook
3. Configure:
   - **Payload URL**: `https://your-domain.com/webhooks/github`
   - **Content type**: `application/json`
   - **Secret**: Same as `GITHUB_WEBHOOK_SECRET` in `.env`
   - **Events**: Select "Let me select individual events" → Check "Pull requests"
   - **Active**: ✅ Checked
4. Click "Add webhook"

### Step 7: Test Webhook

Open or update a PR in your repository. Check logs:

```bash
docker compose logs -f backend worker
```

You should see:
```
backend  | 📥 Received PR event: owner/repo#123 - PR Title
worker   | 🚀 Starting analysis for owner/repo#123
worker   | ✅ Successfully analyzed and commented on owner/repo#123
```

---

## Manual Deployment

### Step 1: Install Dependencies

**Ubuntu/Debian:**
```bash
# Python 3.11+
apt-get update
apt-get install -y python3.11 python3.11-venv python3-pip

# PostgreSQL client
apt-get install -y libpq-dev

# Redis (if hosting yourself)
apt-get install -y redis-server
```

**macOS:**
```bash
brew install python@3.11 postgresql redis
```

### Step 2: Clone & Setup

```bash
git clone https://github.com/sahilKumar1122/PR-Pilot.git
cd PR-Pilot
```

### Step 3: Setup Backend

```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp ../env.example ../.env
nano ../.env

# Run backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Production:** Use a process manager like systemd or supervisor.

**Example systemd service (`/etc/systemd/system/prpilot-backend.service`):**
```ini
[Unit]
Description=PR Pilot Backend
After=network.target

[Service]
Type=simple
User=prpilot
WorkingDirectory=/opt/PR-Pilot/backend
Environment="PATH=/opt/PR-Pilot/backend/venv/bin"
EnvironmentFile=/opt/PR-Pilot/.env
ExecStart=/opt/PR-Pilot/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 4: Setup Worker

```bash
cd ../worker
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run worker
celery -A tasks worker --loglevel=info
```

**Example systemd service (`/etc/systemd/system/prpilot-worker.service`):**
```ini
[Unit]
Description=PR Pilot Worker
After=network.target redis.service postgresql.service

[Service]
Type=simple
User=prpilot
WorkingDirectory=/opt/PR-Pilot/worker
Environment="PATH=/opt/PR-Pilot/worker/venv/bin"
EnvironmentFile=/opt/PR-Pilot/.env
ExecStart=/opt/PR-Pilot/worker/venv/bin/celery -A tasks worker --loglevel=info --concurrency=2
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 5: Setup Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

For HTTPS (recommended), use Let's Encrypt:
```bash
apt-get install certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

---

## Cloud Platform Guides

### AWS

**Option 1: ECS (Elastic Container Service)**

1. Push Docker images to ECR
2. Create ECS cluster
3. Define task definitions for backend + worker
4. Create services with load balancer for backend
5. Use ElastiCache for Redis, RDS for PostgreSQL

**Option 2: EC2**

1. Launch EC2 instance (t3.medium recommended)
2. Follow Docker deployment steps above
3. Configure security groups (port 8000 for webhook)

### Google Cloud Platform

**Option 1: Cloud Run**

```bash
# Build and push
gcloud builds submit --tag gcr.io/your-project/prpilot-backend backend/
gcloud builds submit --tag gcr.io/your-project/prpilot-worker worker/

# Deploy backend
gcloud run deploy prpilot-backend \
  --image gcr.io/your-project/prpilot-backend \
  --set-env-vars REDIS_URL=...,DATABASE_URL=...

# Deploy worker (requires Cloud Run Jobs or Compute Engine)
```

**Option 2: Compute Engine**

Similar to AWS EC2 approach.

### Digital Ocean

**Option 1: App Platform**

1. Connect GitHub repository
2. Configure environment variables
3. Deploy backend as web service
4. Deploy worker as worker component
5. Use Managed Redis + PostgreSQL

**Option 2: Droplet**

1. Create Droplet (2 CPU, 4GB RAM)
2. Follow Docker deployment steps

### Heroku

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login and create app
heroku login
heroku create prpilot-backend

# Add PostgreSQL and Redis
heroku addons:create heroku-postgresql:mini
heroku addons:create heroku-redis:mini

# Configure environment
heroku config:set GITHUB_TOKEN=...
heroku config:set HF_API_KEY=...
heroku config:set GITHUB_WEBHOOK_SECRET=...

# Deploy
git push heroku main

# Scale worker
heroku ps:scale worker=1
```

**Note:** Requires `Procfile`:
```
web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
worker: celery -A worker.tasks worker --loglevel=info
```

---

## Configuration

### Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_TOKEN` | Yes | - | GitHub PAT for API access |
| `HF_API_KEY` | Yes | - | HuggingFace API key |
| `GITHUB_WEBHOOK_SECRET` | Yes* | - | Webhook signature verification |
| `REDIS_URL` | Yes | `redis://localhost:6379/0` | Redis connection string |
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `LOG_LEVEL` | No | `INFO` | Logging level (DEBUG/INFO/WARNING/ERROR) |
| `SENTRY_DSN` | No | - | Sentry error tracking (optional) |

*Technically optional, but **strongly recommended** for production.

### Production Settings

**backend/.env:**
```bash
# Use production Redis
REDIS_URL=redis://prod-redis:6379/0

# Use production database
DATABASE_URL=postgresql://user:pass@prod-db:5432/prpilot

# Enable error tracking
SENTRY_DSN=https://...@sentry.io/...

# Production log level
LOG_LEVEL=INFO
```

---

## Monitoring & Logging

### Application Logs

**Docker:**
```bash
# View all logs
docker compose logs -f

# View specific service
docker compose logs -f backend
docker compose logs -f worker
```

**Manual:**
```bash
# Backend logs
journalctl -u prpilot-backend -f

# Worker logs
journalctl -u prpilot-worker -f
```

### Celery Monitoring

**Flower** (web-based monitoring):
```bash
pip install flower
celery -A worker.tasks flower --port=5555
```

Access at: `http://localhost:5555`

### Error Tracking

**Sentry Integration:**

1. Create account at https://sentry.io
2. Get DSN
3. Add to `.env`:
   ```bash
   SENTRY_DSN=https://...@sentry.io/...
   ```

### Health Monitoring

**Simple script:**
```bash
#!/bin/bash
# health-check.sh

HEALTH_URL="http://localhost:8000/"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ Service healthy"
    exit 0
else
    echo "❌ Service unhealthy (HTTP $RESPONSE)"
    exit 1
fi
```

**Cron job:**
```bash
*/5 * * * * /opt/PR-Pilot/health-check.sh || systemctl restart prpilot-backend
```

---

## Scaling

### Horizontal Scaling

**Backend:**
- Stateless, can scale infinitely
- Run multiple instances behind load balancer
- Each instance handles webhooks independently

**Worker:**
- Easiest to scale
- Add more worker processes/containers
- All workers share same Redis queue

```bash
# Docker Compose: Scale workers
docker compose up -d --scale worker=3

# Manual: Run multiple workers
celery -A tasks worker --concurrency=4 --loglevel=info
```

**Database & Redis:**
- Use managed services (AWS RDS, ElastiCache)
- Enable read replicas for database (if needed)
- Redis typically doesn't need scaling for most workloads

### Vertical Scaling

Increase resources for worker nodes:
- More CPU → Faster AI processing
- More RAM → Handle larger PRs
- Recommended: 2-4 CPU cores, 4-8GB RAM per worker

### Auto-Scaling

**Kubernetes:**
- Deploy backend as Deployment with HPA
- Deploy worker as Deployment with KEDA (scale based on Redis queue length)

**AWS ECS:**
- Target tracking scaling policies
- Scale workers based on SQS queue depth (if using SQS instead of Redis)

---

## Security

### Best Practices

1. **Always set `GITHUB_WEBHOOK_SECRET`**
   ```bash
   # Generate strong secret
   openssl rand -hex 32
   ```

2. **Use HTTPS for webhook endpoint**
   - Let's Encrypt for free SSL
   - Required for production

3. **Restrict API token permissions**
   - GitHub PAT: Only grant `repo` scope
   - HuggingFace: Read-only token

4. **Firewall rules**
   - Only expose port 80/443 (webhook endpoint)
   - Backend port 8000 should not be publicly accessible
   - Redis/PostgreSQL should be internal only

5. **Keep secrets secure**
   - Never commit `.env` to git
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
   - Rotate tokens regularly

6. **Network security**
   - Use VPC/private networks
   - Enable encryption in transit (Redis TLS, PostgreSQL SSL)
   - Enable encryption at rest (database encryption)

7. **Updates**
   - Keep dependencies updated
   - Subscribe to security advisories
   - Run `pip-audit` regularly:
     ```bash
     pip install pip-audit
     pip-audit
     ```

---

## Backup & Recovery

### Database Backups

**PostgreSQL:**
```bash
# Backup
pg_dump -h localhost -U prpilot prpilot > backup.sql

# Restore
psql -h localhost -U prpilot prpilot < backup.sql

# Automated daily backups
0 2 * * * pg_dump ... > backup-$(date +\%Y\%m\%d).sql
```

### Configuration Backups

```bash
# Backup .env and configs
tar -czf config-backup.tar.gz .env docker-compose.yml
```

---

## Troubleshooting

See [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues and solutions.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)
- **Documentation**: [docs/](../docs/)
