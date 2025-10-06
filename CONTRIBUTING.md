# Contributing to PR Pilot

Thank you for your interest in contributing to PR Pilot! 🎉

We love contributions from the community and want to make it as easy as possible to contribute.

---

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/PR-Pilot.git
   cd PR-Pilot
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
4. **Make your changes**
5. **Test your changes**
6. **Commit with conventional commits**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
7. **Push and create a PR**

---

## 💡 How Can I Contribute?

### Reporting Bugs 🐛

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Relevant logs or screenshots

**Use the bug report template when creating the issue.**

### Suggesting Features ✨

We love feature ideas! Please:
- Check existing issues first
- Describe the problem you're trying to solve
- Explain your proposed solution
- Share any examples or mockups

**Use the feature request template.**

### Writing Code 💻

#### Areas We Need Help:

**High Priority:**
- [ ] Interactive commands (@PR-Pilot /review, /suggest)
- [ ] Inline code suggestions
- [ ] Support for GitLab and BitBucket
- [ ] Database models for storing analysis history
- [ ] Dashboard for viewing results

**Medium Priority:**
- [ ] More AI model integrations (GPT-4, Claude, Gemini)
- [ ] Better diff parsing algorithms
- [ ] Test coverage improvements
- [ ] Performance optimizations

**Good First Issues:**
- Look for issues tagged with `good-first-issue`
- Documentation improvements
- Adding examples
- Fixing typos

#### Code Style:

- Follow PEP 8 for Python code
- Use type hints
- Write docstrings for all functions
- Add comments explaining **WHY**, not what
- Keep functions small and focused

#### Testing:

- Add tests for new features
- Ensure existing tests pass: `pytest`
- Test with real PRs when possible

---

## 🏗️ Project Structure

```
PR-Pilot/
├── backend/          # FastAPI webhook server
│   ├── main.py      # Entry point
│   └── routers/     # API routes (future)
├── worker/          # Celery background tasks
│   ├── tasks.py     # Main task definitions
│   ├── integrations/  # External APIs (GitHub, HF)
│   └── analyzers/   # PR analysis logic
├── tests/           # Test files
├── docs/            # Documentation
└── infra/           # Docker and deployment configs
```

---

## 🔄 Development Workflow

### Setting Up Your Environment

1. **Install Python 3.11+**
2. **Create virtual environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Docker services**
   ```bash
   docker-compose up -d
   ```
5. **Set up environment variables**
   ```bash
   cp env.example .env
   # Add your API keys to .env
   ```

### Running Tests

```bash
# All tests
pytest

# Specific test
pytest tests/test_ai_analysis.py

# With coverage
pytest --cov=worker --cov=backend
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Worker:**
```bash
cd worker
celery -A tasks worker --loglevel=info --pool=solo
```

**Terminal 3 - Test:**
```bash
python tests/test_webhook.py
```

---

## 📝 Commit Message Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(analyzer): add inline code suggestions
fix(webhook): handle missing PR body gracefully
docs(readme): add installation video
test(integration): add GitHub API mock tests
```

---

## 🎯 Pull Request Process

1. **Update documentation** if you changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** under "Unreleased"
5. **Fill out the PR template** completely
6. **Link related issues** using keywords (Closes #123)

### PR Checklist:

- [ ] Code follows project style
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commits follow conventional commits
- [ ] No merge conflicts
- [ ] PR description is clear

---

## 🤝 Code of Conduct

Please be respectful and professional. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

---

## 💬 Getting Help

- **Discord**: Join our [community](https://discord.gg/YOUR_LINK) (coming soon!)
- **GitHub Discussions**: Ask questions
- **Issues**: Report bugs or request features
- **Email**: your.email@example.com

---

## 🌟 Recognition

Contributors will be:
- Listed in README.md
- Mentioned in release notes
- Given credit in the project

Thank you for making PR Pilot better! 🎉
