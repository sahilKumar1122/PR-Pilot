# 🎉 PR Pilot v0.1.0 - MVP Launch

**AI-Powered Pull Request Reviews**

PR Pilot automatically analyzes GitHub pull requests using AI, providing intelligent summaries, risk detection, and actionable suggestions - all self-hosted and privacy-first.

---

## ✨ Features

### 🤖 Core Analysis
- **Smart Summarization**: AI-powered PR summaries using HuggingFace models (distilbart, bart-large-cnn)
- **Automatic Classification**: Categorizes PRs as bug fix, feature, refactor, or documentation
- **Risk Detection**: Flags large PRs, many file changes, and sensitive file modifications
- **Test & Doc Suggestions**: Identifies missing test coverage and documentation needs

### 🏗️ Architecture
- **FastAPI Backend**: Lightning-fast webhook endpoint with HMAC-SHA256 signature verification
- **Celery Workers**: Async background processing for long-running AI analysis
- **Redis Queue**: Reliable message broker for task distribution
- **PostgreSQL**: Database for storing analysis history (future)

### 🔒 Privacy & Reliability
- **Self-Hosted**: Your code never leaves your infrastructure
- **Smart Fallbacks**: Keyword-based analysis when AI models timeout
- **Free AI Models**: Uses HuggingFace free tier (no OpenAI costs)
- **Production Ready**: Full Docker support, CI/CD, comprehensive docs

### 🛠️ Developer Experience
- **Easy Setup**: 5-minute Docker Compose deployment
- **Comprehensive Docs**: API reference, deployment guide, troubleshooting
- **CI/CD Pipeline**: GitHub Actions for linting, testing, Docker builds
- **Open Source**: MIT License, welcoming contributions

---

## 📸 Screenshots

> **Coming Soon!** Screenshots will be added shortly. In the meantime:
> - See [Demo Guide](https://github.com/sahilKumar1122/PR-Pilot/blob/main/assets/DEMO_GUIDE.md) for details
> - Try it yourself with the [Quick Start](https://github.com/sahilKumar1122/PR-Pilot#quick-start)

---

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/sahilKumar1122/PR-Pilot.git
cd PR-Pilot

# 2. Configure environment
cp env.example .env
# Edit .env with your GitHub token and HuggingFace API key

# 3. Start services
docker compose up -d

# 4. Verify
curl http://localhost:8000/
# Should return: {"status":"healthy","service":"pr-pilot"}
```

### Configure GitHub Webhook

1. Go to your repo → **Settings** → **Webhooks** → **Add webhook**
2. **Payload URL**: `https://your-domain.com/webhooks/github`
3. **Content type**: `application/json`
4. **Secret**: Same as `GITHUB_WEBHOOK_SECRET` in `.env`
5. **Events**: Select "Pull requests"
6. Click **Add webhook**

That's it! Open a PR and watch PR Pilot analyze it automatically. 🎉

---

## 📚 Documentation

Comprehensive guides for all use cases:

- **[Quick Start Guide](https://github.com/sahilKumar1122/PR-Pilot#quick-start)** - Get running in 5 minutes
- **[API Reference](https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/API.md)** - Complete API documentation
- **[Deployment Guide](https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/DEPLOYMENT.md)** - Deploy to production (Docker, AWS, GCP, Heroku)
- **[Development Guide](https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/DEVELOPMENT.md)** - Contribute to the project
- **[Troubleshooting](https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Changelog](https://github.com/sahilKumar1122/PR-Pilot/blob/main/CHANGELOG.md)** - Version history

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend** | FastAPI 0.104, Uvicorn |
| **Workers** | Celery 5.3, Redis 7 |
| **Database** | PostgreSQL 15 |
| **AI/ML** | HuggingFace Inference API |
| **Container** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Language** | Python 3.11+ |

---

## 🆚 Comparison with Other Tools

| Feature | PR Pilot | GitHub Copilot | PR-Agent (Qodo AI) |
|---------|----------|----------------|-------------------|
| **Self-Hosted** | ✅ Yes | ❌ No | ⚠️ Partial |
| **Open Source** | ✅ MIT | ❌ No | ✅ Apache 2.0 |
| **Free AI Models** | ✅ HuggingFace | ❌ No | ❌ Requires OpenAI |
| **Fallback Mechanisms** | ✅ Smart fallbacks | ❌ No | ❌ No |
| **Privacy** | ✅ 100% self-hosted | ❌ Cloud only | ⚠️ Hybrid |
| **Setup Time** | ✅ 5 minutes | N/A | ⚠️ 15+ minutes |
| **Cost** | ✅ Free | 💰 $10-20/month | 💰 API costs |

---

## 🔄 What's Next?

### Planned for v0.2.0
- Dashboard for reviewing analysis history
- Custom AI model support
- Semantic code search with pgvector
- Multi-language support beyond Python
- Webhook for other Git platforms (GitLab, Bitbucket)

### Planned for v1.0.0
- Advanced security scanning
- Code complexity analysis
- Performance impact prediction
- Integration with CI/CD pipelines
- Team collaboration features

See our [Roadmap](https://github.com/sahilKumar1122/PR-Pilot#roadmap) for details.

---

## 🤝 Contributing

We welcome contributions! PR Pilot is built by developers, for developers.

**Ways to contribute:**
- 🐛 Report bugs or request features via [Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- 💻 Submit pull requests (see [Contributing Guide](https://github.com/sahilKumar1122/PR-Pilot/blob/main/CONTRIBUTING.md))
- 📖 Improve documentation
- ⭐ Star the repo to show support
- 💬 Join [Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)

---

## 🙏 Acknowledgments

Built with these amazing open source projects:
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Celery](https://docs.celeryproject.org/) - Distributed task queue
- [HuggingFace](https://huggingface.co/) - AI model inference
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API client

Inspired by:
- [PR-Agent by Qodo AI](https://github.com/qodo-ai/pr-agent)
- [CodeRabbit](https://coderabbit.ai/)
- [Sweep AI](https://sweep.dev/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/sahilKumar1122/PR-Pilot/blob/main/LICENSE) file for details.

---

## 💬 Support

- **Documentation**: [docs/](https://github.com/sahilKumar1122/PR-Pilot/tree/main/docs)
- **Issues**: [GitHub Issues](https://github.com/sahilKumar1122/PR-Pilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/sahilKumar1122/PR-Pilot/discussions)
- **Email**: [Your email or leave blank]

---

## 🌟 Star History

If you find PR Pilot useful, please consider starring the repo! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=sahilKumar1122/PR-Pilot&type=Date)](https://star-history.com/#sahilKumar1122/PR-Pilot&Date)

---

**Made with ❤️ by developers, for developers**

Try PR Pilot today and revolutionize your code review process!
