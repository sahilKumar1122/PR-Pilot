# PR Pilot 🚀

**AI-powered pull request reviewer that summarizes diffs, flags risks, suggests tests/docs, and generates commit messages & release notes.**

[![CI](https://github.com/YOUR_USERNAME/PR-Pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/PR-Pilot/actions/workflows/ci.yml)

---

## Features (MVP)

- 🤖 **Automated PR Analysis**: Webhook-driven analysis of GitHub pull requests
- 📝 **Smart Summaries**: Human-readable PR summaries using NLG models
- 🏷️ **Intent Classification**: Automatically categorize PRs (bug/feature/refactor/docs)
- 💬 **Commit Message Suggestions**: Conventional Commits style suggestions
- ⚠️ **Risk Detection**: Identify potential issues and security concerns
- 🧪 **Test & Docs Suggestions**: Detect missing test coverage and documentation
- 📊 **Dashboard**: Review and provide feedback on AI suggestions

---

## Architecture

```
┌─────────────┐
│   GitHub    │
│   Webhook   │
└──────┬──────┘
       │
       v
┌─────────────────┐
│  FastAPI        │
│  Webhook Server │
└────────┬────────┘
         │
         v
┌─────────────────┐      ┌──────────────┐
│  Redis Queue    │◄─────┤ Celery Worker│
└─────────────────┘      └──────┬───────┘
                                │
                                v
                         ┌─────────────┐
                         │  Postgres   │
                         │  + pgvector │
                         └─────────────┘
                                │
                                v
                         ┌─────────────┐
                         │  Next.js    │
                         │  Dashboard  │
                         └─────────────┘
```

**Tech Stack:**
- **Backend**: FastAPI (Python 3.11+), Uvicorn
- **Worker**: Celery + Redis
- **Database**: PostgreSQL with pgvector extension
- **AI/ML**: Hugging Face Inference API
- **Frontend**: Next.js (optional dashboard)
- **Observability**: Sentry, Prometheus

---

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- GitHub account with a test repository
- Hugging Face API key

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PR-Pilot.git
   cd PR-Pilot
   ```

2. **Copy environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Set up ngrok for local webhook testing**
   ```bash
   ngrok http 8000
   # Copy the HTTPS URL to your GitHub webhook configuration
   ```

6. **Configure GitHub Webhook**
   - Go to your test repo → Settings → Webhooks → Add webhook
   - Payload URL: `https://YOUR_NGROK_URL.ngrok.io/webhooks/github`
   - Content type: `application/json`
   - Secret: Use the value from your `.env` file (`GITHUB_WEBHOOK_SECRET`)
   - Events: Select "Pull requests"

7. **Test it out!**
   - Open a PR in your test repository
   - Watch the logs: `docker-compose logs -f backend worker`
   - Check for the AI-generated comment on your PR

---

## Environment Variables

See `.env.example` for the complete list. Key variables:

### GitHub Configuration
- `GITHUB_APP_ID`: GitHub App ID (recommended) or leave empty for PAT
- `GITHUB_PRIVATE_KEY`: GitHub App private key (base64 encoded)
- `GITHUB_WEBHOOK_SECRET`: Secret for webhook signature verification
- `GITHUB_TOKEN`: Personal Access Token (for initial testing)

### AI/ML Configuration
- `HF_API_KEY`: Hugging Face API key for model inference

### Database & Queue
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string for Celery

### Observability
- `SENTRY_DSN`: Sentry DSN for error tracking (optional)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

---

## Project Structure

```
PR-Pilot/
├── backend/                 # FastAPI application
│   ├── main.py             # Application entry point
│   ├── routers/            # API routes
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   └── utils/              # Helper functions
├── worker/                 # Celery workers
│   ├── tasks.py            # Celery tasks
│   ├── analyzers/          # PR analysis modules
│   └── integrations/       # External API integrations
├── web/                    # Next.js dashboard (optional)
│   ├── pages/
│   ├── components/
│   └── lib/
├── infra/                  # Infrastructure configs
│   ├── docker/
│   └── k8s/
├── tests/                  # Test suites
├── migrations/             # Alembic database migrations
├── docker-compose.yml      # Local development setup
├── .env.example           # Environment template
└── README.md              # This file
```

---

## Development Workflow

### Running Tests
```bash
# Backend tests
docker-compose exec backend pytest

# With coverage
docker-compose exec backend pytest --cov=backend tests/
```

### Database Migrations
```bash
# Create a new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

### Code Quality
```bash
# Linting
docker-compose exec backend ruff check .

# Formatting
docker-compose exec backend black .

# Type checking
docker-compose exec backend mypy .
```

---

## API Endpoints

### Webhooks
- `POST /webhooks/github` - GitHub webhook receiver

### Management (Dashboard API)
- `GET /api/prs` - List processed PRs
- `GET /api/prs/{pr_id}` - Get PR analysis details
- `POST /api/feedback` - Submit feedback on suggestions
- `GET /api/stats` - Get system statistics

---

## Deployment

### Docker Production Build
```bash
docker build -t pr-pilot-backend ./backend
docker build -t pr-pilot-worker ./worker
```

### Deploy to Cloud Run / Render
See `infra/` directory for deployment manifests and instructions.

### GitHub App Setup (Recommended)
1. Create a GitHub App in your organization settings
2. Set permissions: Pull requests (Read & Write), Contents (Read), Webhooks (Read)
3. Generate and download private key
4. Install the app on target repositories
5. Configure environment variables with App ID and private key

---

## Roadmap

- [x] **Sprint 0: Project scaffolding & infrastructure** ✅
  - FastAPI webhook endpoint with signature verification
  - Celery worker setup with Redis
  - Docker Compose infrastructure
  - End-to-end pipeline tested
  
- [x] **Sprint 1: Core PR processing pipeline** ✅
  - GitHub API integration (fetch PRs, post comments)
  - HuggingFace AI integration (summarization, classification)
  - Risk detection and suggestions
  - Commit message generation
  - Smart fallbacks for reliability
  
- [ ] **Sprint 2: Enhanced suggestions & feedback loop** (Upcoming)
  - Interactive commands (@PR-Pilot /review, /suggest)
  - Inline code comments
  - User feedback collection
  - Database models for history
  
- [ ] **Sprint 3: Semantic search & release notes** (Future)
  - Vector database for similar PRs
  - Release notes generation
  - Multi-language support

**Current Status:** ✅ **MVP Complete & Functional!**

See [LEARNING_NOTES.md](./docs/LEARNING_NOTES.md) for detailed development journey.

---

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request (and let PR Pilot review it! 🎯)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Metrics & Observability

Key metrics tracked:
- `avg_time_to_comment`: Time from PR open to bot comment
- `model_latency`: AI model response times
- `num_prs_with_missing_tests`: PRs flagged for missing tests
- `feedback_accept_rate`: Percentage of accepted suggestions
- `false_positive_rate`: Tracked via human feedback

---

## Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [Celery](https://docs.celeryq.dev/)
- [Hugging Face](https://huggingface.co/)
- [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector)

---

## Support

- 📧 Email: ksahilbazard@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)

---

**Made with ❤️ for better code reviews**

