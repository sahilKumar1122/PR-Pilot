# API Documentation

## Overview

PR Pilot exposes a FastAPI-based webhook endpoint for GitHub integration. The API is designed to be lightweight, secure, and responds quickly to webhook events.

## Base URL

```
http://localhost:8000  # Local development
https://your-domain.com  # Production
```

## Interactive Documentation

FastAPI provides auto-generated interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Endpoints

### Health Check

**GET /** 

Check if the service is running.

**Response:**
```json
{
  "status": "healthy",
  "service": "pr-pilot"
}
```

**Status Codes:**
- `200 OK`: Service is healthy

---

### GitHub Webhook

**POST /webhooks/github**

Receives webhook events from GitHub when pull requests are opened, updated, or reopened.

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| `X-Hub-Signature-256` | Yes* | GitHub's HMAC-SHA256 signature for webhook verification |
| `Content-Type` | Yes | Must be `application/json` |

*Required only if `GITHUB_WEBHOOK_SECRET` is configured (recommended for production)

**Request Body:**

GitHub sends a JSON payload containing PR details. Key fields we use:

```json
{
  "action": "opened|synchronize|reopened",
  "pull_request": {
    "number": 123,
    "title": "Add new feature",
    "body": "Description...",
    "html_url": "https://github.com/owner/repo/pull/123"
  },
  "repository": {
    "full_name": "owner/repo-name"
  }
}
```

**Response:**

```json
{
  "status": "enqueued",
  "repo": "owner/repo-name",
  "pr_number": 123,
  "action": "opened",
  "task_id": "abc-123-def-456"
}
```

**Status Codes:**
- `200 OK`: Webhook received and task enqueued
- `401 Unauthorized`: Invalid or missing signature
- `422 Unprocessable Entity`: Invalid payload format

**Actions We Handle:**
- `opened`: New PR created
- `synchronize`: PR updated with new commits
- `reopened`: Closed PR reopened

Other actions (e.g., `closed`, `commented`) are ignored with response:
```json
{
  "status": "ignored",
  "action": "closed"
}
```

---

## Security

### Webhook Signature Verification

PR Pilot verifies that webhook requests come from GitHub using HMAC-SHA256 signatures.

**How it works:**

1. GitHub signs the webhook payload with your `GITHUB_WEBHOOK_SECRET`
2. The signature is sent in the `X-Hub-Signature-256` header
3. PR Pilot recomputes the signature and compares using constant-time comparison
4. If signatures don't match, request is rejected with `401 Unauthorized`

**Setup:**

1. In your GitHub repo: Settings → Webhooks → Add webhook
2. Set the same secret in both places:
   - GitHub webhook configuration
   - Your `.env` file: `GITHUB_WEBHOOK_SECRET=your-secret-here`

**Warning:** If `GITHUB_WEBHOOK_SECRET` is not set, signature verification is skipped. This is only acceptable for local testing!

---

## Task Processing Flow

```
GitHub → Webhook → FastAPI → Celery Queue → Worker → AI Analysis → GitHub Comment
         (instant)            (async)        (30-60s)              (posted)
```

1. **Webhook received** (< 1s): FastAPI validates and enqueues task
2. **Task queued**: Stored in Redis, returns task ID immediately
3. **Worker picks up task** (within seconds): Background processing starts
4. **AI Analysis** (30-60s): Fetches diff, runs AI models, generates suggestions
5. **Comment posted**: Results posted back to GitHub PR

---

## Rate Limiting

**GitHub Webhooks:**
- No rate limiting on our side
- Handle webhooks as fast as GitHub sends them
- Tasks processed async, so webhook endpoint never blocks

**GitHub API (Worker):**
- Rate limit: 5,000 requests/hour (authenticated)
- PR Pilot typically uses 2-3 requests per PR analysis
- Can handle ~1,500-2,000 PRs per hour

**HuggingFace API:**
- Free tier: Rate-limited (exact limits vary by model)
- Fallback mechanisms in place if models timeout
- Consider HuggingFace Pro for higher limits

---

## Error Handling

### Webhook Endpoint

- **Invalid signature**: Returns `401 Unauthorized`
- **Malformed JSON**: Returns `422 Unprocessable Entity`
- **Redis connection error**: Returns `500 Internal Server Error`
- **Any unexpected error**: Logs error, returns `500`

### Worker Tasks

- **Automatic retries**: Up to 3 attempts with 60s backoff
- **GitHub API errors**: Logged, task marked as failed
- **AI model timeout**: Falls back to simpler analysis
- **Network errors**: Retried automatically

---

## Monitoring

### Health Checks

```bash
# Check if backend is running
curl http://localhost:8000/

# Expected response:
{"status":"healthy","service":"pr-pilot"}
```

### Task Status

Currently, task status must be checked via Celery CLI or Redis:

```bash
# In worker container
celery -A tasks inspect active
celery -A tasks inspect stats
```

**Future Enhancement:** Add `/tasks/{task_id}` endpoint to check status via API.

---

## Development

### Running Locally

```bash
# Start all services
docker compose up -d

# Backend available at:
http://localhost:8000

# View logs
docker compose logs -f backend
docker compose logs -f worker
```

### Testing Webhooks

Use the test script:

```bash
python tests/test_webhook.py
```

Or manually with `curl`:

```bash
curl -X POST http://localhost:8000/webhooks/github \
  -H "Content-Type: application/json" \
  -d '{
    "action": "opened",
    "pull_request": {
      "number": 123,
      "title": "Test PR"
    },
    "repository": {
      "full_name": "owner/repo"
    }
  }'
```

---

## API Clients

### Python

```python
import requests

# Trigger webhook
response = requests.post(
    "http://localhost:8000/webhooks/github",
    json={
        "action": "opened",
        "pull_request": {"number": 123, "title": "Test"},
        "repository": {"full_name": "owner/repo"}
    }
)

print(response.json())
# {'status': 'enqueued', 'task_id': '...'}
```

### JavaScript

```javascript
// Trigger webhook
const response = await fetch('http://localhost:8000/webhooks/github', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    action: 'opened',
    pull_request: { number: 123, title: 'Test' },
    repository: { full_name: 'owner/repo' }
  })
});

const data = await response.json();
console.log(data.task_id);
```

---

## OpenAPI Schema

The full OpenAPI schema is available at:

```
http://localhost:8000/openapi.json
```

You can use this to generate client libraries in any language using tools like:
- [OpenAPI Generator](https://openapi-generator.tech/)
- [Swagger Codegen](https://swagger.io/tools/swagger-codegen/)

---

## Future API Endpoints

Planned for future releases:

- `GET /tasks/{task_id}`: Check analysis task status
- `GET /analysis/{repo}/{pr_number}`: Retrieve past analysis results
- `POST /analyze`: Manually trigger analysis (without webhook)
- `GET /stats`: System statistics and metrics
- `POST /feedback/{analysis_id}`: Submit feedback on analysis quality

---

## Support

- **Documentation**: [docs/](../docs/)
- **Issues**: [GitHub Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)
