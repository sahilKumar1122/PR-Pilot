# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive documentation suite:
  - API Reference (docs/API.md)
  - Deployment Guide (docs/DEPLOYMENT.md)
  - Development Guide (docs/DEVELOPMENT.md)
  - Troubleshooting Guide (docs/TROUBLESHOOTING.md)
- Documentation section in README with quick links

### Changed
- Improved README structure with better navigation

## [0.1.0] - 2025-10-06

### Added
- 🎉 Initial release of PR Pilot!
- FastAPI webhook endpoint with HMAC-SHA256 signature verification
- Celery worker for async PR processing
- Docker Compose setup with PostgreSQL and Redis
- GitHub API integration for fetching PRs and posting comments
- HuggingFace AI integration for:
  - PR summarization using distilbart and bart-large-cnn
  - Zero-shot classification (bug/feature/refactor/docs)
- Smart fallback mechanisms when AI models fail:
  - Keyword-based classification
  - Text extraction for summaries
- PR risk detection:
  - Large PR warnings (500+ lines)
  - Many files changed alerts
  - Sensitive file detection (config, secrets, etc.)
- Test and documentation suggestions
- Conventional commit message generation
- Beautiful markdown comment formatting
- Comprehensive test suite
- SSL verification handling for corporate networks

### Documentation
- Complete README with architecture and setup instructions
- CONTRIBUTING.md with development guidelines
- CODE_OF_CONDUCT.md
- LEARNING_NOTES.md documenting the development journey
- GitHub issue and PR templates
- CI/CD setup with GitHub Actions

### Infrastructure
- Docker Compose for local development
- Redis for job queue
- PostgreSQL for database (pgvector ready for future)
- Automated testing with pytest
- Code quality checks (ruff, black, mypy)

## [0.0.1] - 2025-10-03

### Added
- Project initialization
- Basic project structure
- Sprint 0 infrastructure setup

---

## Release Notes

### v0.1.0 - "The MVP Release" 🚀

This is the first functional release of PR Pilot! The core pipeline is complete and working:

**GitHub Webhook → FastAPI → Redis → Celery → AI Analysis → GitHub Comment**

**What Works:**
- ✅ Automatically analyzes PRs when opened/updated
- ✅ AI-powered summarization and classification
- ✅ Risk detection and suggestions
- ✅ Reliable with smart fallbacks
- ✅ Beautiful, informative PR comments

**What's Next (v0.2.0):**
- Interactive commands (@PR-Pilot /review, /suggest)
- Inline code suggestions
- Database models for history tracking
- User feedback collection
- Dashboard for viewing results

**Known Limitations:**
- GitHub only (no GitLab/BitBucket yet)
- Single comprehensive comment (no inline comments)
- HuggingFace models may timeout in corporate networks
- No persistent storage of analysis results yet

**Try It:**
```bash
git clone https://github.com/sahilKumar1122/PR-Pilot.git
cd PR-Pilot
# Follow README.md for setup
```

---

[Unreleased]: https://github.com/sahilKumar1122/PR-Pilot/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/sahilKumar1122/PR-Pilot/releases/tag/v0.1.0
[0.0.1]: https://github.com/sahilKumar1122/PR-Pilot/releases/tag/v0.0.1
