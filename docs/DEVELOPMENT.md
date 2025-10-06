# Development Guide

Guide for developers who want to contribute to PR Pilot or understand the codebase.

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Adding New Features](#adding-new-features)
- [Database Migrations](#database-migrations)
- [Release Process](#release-process)

---

## Project Structure

```
PR-Pilot/
├── backend/                 # FastAPI webhook server
│   ├── main.py             # Entry point, webhook endpoint
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container image
│
├── worker/                  # Celery background tasks
│   ├── tasks.py            # Main Celery tasks
│   ├── analyzers/          # PR analysis logic
│   │   └── pr_analyzer.py  # Core analysis orchestration
│   ├── integrations/       # External API clients
│   │   ├── github_client.py    # GitHub API wrapper
│   │   └── huggingface_client.py # HuggingFace API wrapper
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Worker container image
│
├── tests/                   # Test scripts
│   ├── test_webhook.py     # Webhook simulation
│   ├── test_connections.py # Infrastructure tests
│   └── test_ai_analysis.py # End-to-end test
│
├── docs/                    # Documentation
│   ├── API.md              # API reference
│   ├── DEPLOYMENT.md       # Deployment guide
│   ├── TROUBLESHOOTING.md  # Common issues
│   └── DEVELOPMENT.md      # This file
│
├── .github/                 # GitHub Actions & templates
│   ├── workflows/
│   │   └── ci.yml          # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/     # Issue templates
│   └── pull_request_template.md
│
├── docker-compose.yml       # Local development orchestration
├── .env.example            # Environment template
├── README.md               # Project overview
├── CONTRIBUTING.md         # Contribution guidelines
├── CODE_OF_CONDUCT.md      # Community guidelines
├── CHANGELOG.md            # Version history
└── LICENSE                 # MIT License
```

---

## Architecture Overview

### High-Level Flow

```
┌─────────┐    webhook     ┌─────────┐    enqueue    ┌───────┐
│ GitHub  │───────────────▶│ Backend │──────────────▶│ Redis │
│   PR    │                │ FastAPI │               │ Queue │
└─────────┘                └─────────┘               └───────┘
                                                          │
                                                          │ consume
                                                          ▼
    ┌─────────────────────────────────────────────┬───────────┐
    │                                             │  Worker   │
    │  1. Fetch PR diff (GitHub API)              │  (Celery) │
    │  2. Parse changes                           │           │
    │  3. AI summarization (HuggingFace)          │           │
    │  4. Risk classification (AI)                │           │
    │  5. Generate suggestions                    │           │
    │  6. Format comment                          │           │
    │  7. Post to GitHub                          │           │
    └─────────────────────────────────────────────┴───────────┘
                              │
                              ▼
                        ┌──────────┐
                        │  GitHub  │
                        │ Comment  │
                        └──────────┘
```

### Component Responsibilities

**Backend (`backend/main.py`):**
- ✅ Receive webhook events
- ✅ Validate signatures (HMAC-SHA256)
- ✅ Enqueue jobs quickly (< 1s response time)
- ❌ NO heavy processing
- ❌ NO AI inference

**Worker (`worker/tasks.py`):**
- ✅ Process PR analysis (30-60s)
- ✅ Call external APIs (GitHub, HuggingFace)
- ✅ Retry on failures
- ✅ Post results back to GitHub

**Redis:**
- Message broker for Celery
- Stores task queue and results

**PostgreSQL:**
- Future: Store PR metadata, analysis history
- Current: Not heavily used (v0.1.0)

---

## Development Setup

### Prerequisites

- Python 3.11 or 3.12 (3.13 works too)
- Docker & Docker Compose
- Git
- Code editor (VS Code recommended)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/sahilKumar1122/PR-Pilot.git
cd PR-Pilot

# Create .env file
cp env.example .env
# Edit .env with your tokens
```

### Option 1: Docker Development (Recommended)

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Code changes auto-reload (volume mounts enabled)
```

**Pros:**
- Consistent environment
- All services managed together
- Auto-reload on code changes

**Cons:**
- Need to rebuild for dependency changes
- Slightly slower on Windows

### Option 2: Local Development

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --port 8000
```

**Worker:**
```bash
cd worker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run worker
celery -A tasks worker --loglevel=info
```

**Redis & PostgreSQL:**
```bash
# Still use Docker for infrastructure
docker compose up -d redis postgres
```

**Pros:**
- Faster iteration
- Native debugger support
- Lower resource usage

**Cons:**
- Manual service management
- Platform-specific issues

### VS Code Setup

**.vscode/settings.json:**
```json
{
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "[python]": {
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

**.vscode/launch.json:**
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Backend: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--reload",
        "--port",
        "8000"
      ],
      "cwd": "${workspaceFolder}/backend",
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal"
    },
    {
      "name": "Worker: Celery",
      "type": "python",
      "request": "launch",
      "module": "celery",
      "args": [
        "-A",
        "tasks",
        "worker",
        "--loglevel=debug"
      ],
      "cwd": "${workspaceFolder}/worker",
      "envFile": "${workspaceFolder}/.env",
      "console": "integratedTerminal"
    }
  ]
}
```

---

## Code Style

### Python Style Guide

We follow **PEP 8** with some customizations:

- **Line length**: 88 characters (Black default)
- **Quotes**: Double quotes preferred
- **Imports**: Sorted with `isort`
- **Type hints**: Use where helpful (not required for v0.1.0)

### Formatters & Linters

```bash
# Install tools (already in requirements.txt)
pip install black isort ruff

# Format code
black backend/ worker/ tests/
isort backend/ worker/ tests/

# Lint code
ruff check backend/ worker/ tests/

# Fix auto-fixable issues
ruff check backend/ worker/ tests/ --fix
```

### Pre-commit Hooks (Optional)

```bash
pip install pre-commit

# .pre-commit-config.yaml (create this)
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff

# Install hooks
pre-commit install
```

### Documentation Style

- Use **Markdown** for all docs
- Include code examples
- Keep language simple and clear
- Add emojis sparingly (for visual markers)

---

## Testing

### Test Structure

```
tests/
├── test_webhook.py         # Simulates GitHub webhooks
├── test_connections.py     # Tests Redis/PostgreSQL
├── test_ai_analysis.py     # Full E2E test
└── conftest.py             # Pytest fixtures (future)
```

### Running Tests

**Manual test scripts:**
```bash
# Test connections
python tests/test_connections.py

# Test full analysis pipeline
python tests/test_ai_analysis.py

# Simulate webhook
python tests/test_webhook.py
```

**Future (pytest):**
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=backend --cov=worker

# Run specific test
pytest tests/test_webhook.py -v
```

### Writing Tests

**Example test (future):**
```python
# tests/test_backend.py
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "pr-pilot"
    }

def test_webhook_invalid_signature():
    response = client.post(
        "/webhooks/github",
        json={"action": "opened"},
        headers={"X-Hub-Signature-256": "invalid"}
    )
    assert response.status_code == 401
```

### CI/CD Tests

GitHub Actions runs tests automatically:

```yaml
# .github/workflows/ci.yml
- Test: Python 3.11, 3.12, 3.13
- Lint: black, isort, ruff
- Docker: Build and health checks
```

---

## Adding New Features

### Example: Add New AI Analysis

**1. Update `worker/analyzers/pr_analyzer.py`:**

```python
def _detect_security_issues(self, files: List[str], diff: str) -> List[str]:
    """New feature: Detect potential security issues"""
    issues = []
    
    # Check for common security patterns
    if "password" in diff.lower() or "api_key" in diff.lower():
        issues.append("⚠️ Potential hardcoded secrets detected")
    
    if ".env" in files:
        issues.append("⚠️ Environment file modified - review carefully")
    
    # TODO: Use AI model for deeper analysis
    
    return issues

def analyze(self, repo: str, pr_number: int) -> dict:
    # ... existing code ...
    
    # Add new analysis
    security_issues = self._detect_security_issues(
        analysis["files_changed"],
        diff_data["diff"]
    )
    
    analysis["security_issues"] = security_issues
    return analysis
```

**2. Update comment format in `format_comment()`:**

```python
if analysis.get("security_issues"):
    comment += "\n### 🔒 Security Concerns\n"
    for issue in analysis["security_issues"]:
        comment += f"- {issue}\n"
```

**3. Add test:**

```python
# tests/test_security_detection.py
def test_detect_hardcoded_secrets():
    analyzer = PRAnalyzer()
    files = ["config.py"]
    diff = "password = 'hardcoded123'"
    
    issues = analyzer._detect_security_issues(files, diff)
    assert len(issues) > 0
    assert "secrets" in issues[0].lower()
```

**4. Update CHANGELOG.md:**

```markdown
### Added
- Security issue detection in PR analysis
```

### Example: Add New Integration

**1. Create client:**

```python
# worker/integrations/slack_client.py
import os
import requests

class SlackClient:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    
    def send_notification(self, message: str):
        """Send notification to Slack"""
        payload = {"text": message}
        response = requests.post(self.webhook_url, json=payload)
        return response.status_code == 200
```

**2. Use in worker:**

```python
# worker/tasks.py
from worker.integrations.slack_client import SlackClient

@celery_app.task(bind=True, max_retries=3)
def analyze_pr(self, repo: str, pr_number: int, payload: dict):
    # ... existing analysis ...
    
    # Send notification
    slack = SlackClient()
    slack.send_notification(
        f"✅ Analyzed {repo}#{pr_number}: {analysis['summary']}"
    )
```

**3. Document in README.md and .env.example**

---

## Database Migrations

Currently, PR Pilot doesn't heavily use PostgreSQL, but when we add database models:

**Using Alembic:**

```bash
# Initialize (already done)
cd backend
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add pr_analyses table"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

**Example model:**

```python
# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PRAnalysis(Base):
    __tablename__ = "pr_analyses"
    
    id = Column(Integer, primary_key=True)
    repo = Column(String, nullable=False)
    pr_number = Column(Integer, nullable=False)
    summary = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
```

---

## Release Process

### Versioning

We follow **Semantic Versioning** (SemVer):

- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features (backward compatible)
- **PATCH** (0.1.1): Bug fixes

### Creating a Release

**1. Update CHANGELOG.md:**

```markdown
## [0.2.0] - 2024-12-XX

### Added
- Feature X
- Feature Y

### Changed
- Improvement Z

### Fixed
- Bug fix W
```

**2. Update version in code:**

```python
# backend/main.py
app = FastAPI(
    title="PR Pilot API",
    description="AI-powered PR review",
    version="0.2.0",  # Update here
)
```

**3. Commit changes:**

```bash
git add .
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

**4. Create tag:**

```bash
git tag -a v0.2.0 -m "Release v0.2.0

Detailed release notes here...
"

git push origin v0.2.0
```

**5. Create GitHub Release:**

- Go to: https://github.com/sahilKumar1122/PR-Pilot/releases
- Click "Draft a new release"
- Choose tag: `v0.2.0`
- Title: "🚀 PR Pilot v0.2.0"
- Description: Copy from CHANGELOG.md
- Attach binaries if applicable
- Click "Publish release"

**6. Announce:**

- GitHub Discussions
- Twitter/X
- Dev.to blog post
- Reddit (r/opensource, r/python)

---

## Debugging

### Backend Debugging

```python
# backend/main.py
import pdb; pdb.set_trace()  # Add breakpoint

# Or use VS Code debugger (see launch.json above)
```

### Worker Debugging

```bash
# Run worker in foreground with debug logging
celery -A tasks worker --loglevel=debug

# Test single task
python -c "
from worker.tasks import analyze_pr
result = analyze_pr('owner/repo', 123, {})
print(result)
"
```

### Remote Debugging (Production)

```python
# Add to worker/tasks.py (temporarily!)
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use Sentry for production errors
import sentry_sdk
sentry_sdk.init(dsn="...")
```

---

## Performance Optimization

### Profiling

```bash
# Install profiler
pip install py-spy

# Profile worker
py-spy record -o profile.svg -- celery -A tasks worker

# View profile.svg in browser
```

### Caching

```python
# Future: Cache GitHub API responses
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_pr_diff(repo: str, pr_number: int):
    # ... fetch from GitHub ...
    pass
```

### Async Operations

```python
# Future: Make AI calls concurrent
import asyncio

async def analyze_concurrent(diff):
    summary_task = asyncio.create_task(summarize(diff))
    classify_task = asyncio.create_task(classify(diff))
    
    summary = await summary_task
    classification = await classify_task
    return summary, classification
```

---

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code of Conduct
- How to submit issues
- How to submit PRs
- Communication channels

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Celery Docs**: https://docs.celeryproject.org/
- **HuggingFace Docs**: https://huggingface.co/docs
- **GitHub API**: https://docs.github.com/en/rest
- **Docker Compose**: https://docs.docker.com/compose/

---

## Questions?

- **GitHub Discussions**: https://github.com/sahilKumar1122/PR-Pilot/discussions
- **Issues**: https://github.com/sahilKumar1122/PR-Pilot/issues
