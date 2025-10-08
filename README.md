# PR Pilot 🤖

<div align="center">

**AI-powered pull request reviewer that automatically analyzes diffs, flags risks, suggests tests/docs, and generates commit messages.**

[![CI](https://github.com/sahilKumar1122/PR-Pilot/actions/workflows/ci.yml/badge.svg)](https://github.com/sahilKumar1122/PR-Pilot/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#features-mvp) • [Quick Start](#quick-start) • [Demo](#demo) • [Documentation](#documentation) • [Contributing](#contributing)

</div>

---

## ✨ Why PR Pilot?

🚀 **Automated Analysis**: No manual reviews needed - PR Pilot analyzes every PR automatically  
🤖 **AI-Powered**: Uses HuggingFace models for intelligent summarization and classification  
🔒 **Privacy-First**: Self-hosted with your own API keys - your code never leaves your infrastructure  
💰 **Cost-Effective**: Free HuggingFace models, no expensive OpenAI credits needed  
⚡ **Fast & Reliable**: Smart fallbacks ensure it works even when AI models are slow  
🎯 **Actionable**: Risk detection, test suggestions, and commit message generation

---

## 🎥 Demo

### Video Demo (Coming Soon!)

> 📹 **Demo video in progress!** Check back soon or [follow the guide](assets/DEMO_GUIDE.md) to see it in action.

### Screenshots

<details>
<summary>🤖 <b>PR Analysis Comment</b> (Click to expand)</summary>

> **Screenshot coming soon!** This will show PR Pilot's AI-generated analysis comment on a pull request.

**What it includes:**
- 📝 AI-powered summary of changes
- 🏷️ Automatic classification (bug/feature/refactor/docs)
- 📁 List of files changed
- ⚠️ Risk detection and warnings
- 🧪 Test and documentation suggestions

</details>

<details>
<summary>⚙️ <b>GitHub Webhook Setup</b> (Click to expand)</summary>

> **Screenshot coming soon!** This will show the GitHub webhook configuration.

**Configuration:**
- Webhook URL pointing to PR Pilot
- Content type: `application/json`
- Secret configured for security
- Listening to Pull Request events

</details>

<details>
<summary>🐳 <b>Docker Services Running</b> (Click to expand)</summary>

> **Screenshot coming soon!** This will show all PR Pilot services running via Docker Compose.

**Services:**
- ✅ Backend (FastAPI webhook server)
- ✅ Worker (Celery task processor)
- ✅ PostgreSQL (Database)
- ✅ Redis (Message queue)

</details>

### Try It Yourself!

**Want to see it in action right now?**

1. Fork this repo
2. Follow the [Quick Start](#quick-start) guide (5 minutes)
3. Open a test PR in your repository
4. Watch PR Pilot analyze and comment automatically! ⚡

**Pro tip:** Use the test script for a quick demo:
```bash
python tests/test_ai_analysis.py
```

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

## 📚 Documentation

Comprehensive guides for all aspects of PR Pilot:

- **[API Reference](docs/API.md)** - Complete API documentation, endpoints, authentication
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deploy to production (Docker, Cloud platforms, manual)
- **[Development Guide](docs/DEVELOPMENT.md)** - Contribute to PR Pilot, codebase overview
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

**Quick Links:**
- 🚀 [Quick Start Guide](#quick-start) (above)
- 🏗️ [Architecture](#architecture) (above)
- 📝 [Changelog](CHANGELOG.md)
- 🐛 [Report Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- 💬 [Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)

---

## API Endpoints

### Webhooks
- `POST /webhooks/github` - GitHub webhook receiver

### Management (Dashboard API - Future)
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

## 🤝 Contributing

We love contributions! Whether it's:
- 🐛 Bug reports
- 💡 Feature suggestions
- 📝 Documentation improvements
- 🔧 Code contributions

**See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.**

### Good First Issues

Looking for a place to start? Check out issues tagged with [`good-first-issue`](https://github.com/sahilKumar1122/PR-Pilot/labels/good-first-issue).

### Contributors

<a href="https://github.com/sahilKumar1122/PR-Pilot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sahilKumar1122/PR-Pilot" />
</a>

---

## 🗺️ Comparison with Other Tools

| Feature | PR Pilot | PR-Agent (Qodo) | Copilot |
|---------|----------|-----------------|---------|
| **Cost** | Free (self-hosted) | Free tier (75/mo) | $$$ |
| **AI Models** | HuggingFace (open) | GPT-4/Claude | Copilot |
| **Privacy** | 100% self-hosted | Zero retention | Microsoft |
| **Platforms** | GitHub | GitHub/GitLab/BB | GitHub |
| **Setup** | Docker Compose | GitHub App | Built-in |
| **Customization** | Full control | Limited | None |
| **Learning** | ✅ Great | ❌ Complex | ❌ Black box |

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

## 📞 Support & Community

- 🐛 **Bug Reports**: [Create an issue](https://github.com/sahilKumar1122/PR-Pilot/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [Suggest a feature](https://github.com/sahilKumar1122/PR-Pilot/issues/new?template=feature_request.md)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)
- 📧 **Email**: ksahilbazard@gmail.com
- 📖 **Documentation**: [Wiki](https://github.com/sahilKumar1122/PR-Pilot/wiki) (coming soon!)

### Star History

If you find PR Pilot useful, please consider giving it a ⭐!

[![Star History Chart](https://api.star-history.com/svg?repos=sahilKumar1122/PR-Pilot&type=Date)](https://star-history.com/#sahilKumar1122/PR-Pilot&Date)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Celery](https://docs.celeryq.dev/) - Distributed task queue
- [HuggingFace](https://huggingface.co/) - AI models and inference
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API client
- [PostgreSQL](https://www.postgresql.org/) + [pgvector](https://github.com/pgvector/pgvector) - Database

Inspired by [PR-Agent](https://github.com/qodo-ai/pr-agent) and the amazing open source community!

---

<div align="center">

**Made with ❤️ for better code reviews**

[⬆ Back to Top](#pr-pilot-)

</div>

