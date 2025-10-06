# PR Pilot - Learning Notes

This document tracks what we learn as we build this project together.

## Sprint 0: Project Setup

### ✅ What We've Done
- Created project structure with backend/, worker/, infra/, tests/, docs/
- Understood why we separate webhook receiver from worker (speed vs. heavy processing)

### 🎓 Key Concepts Learned

#### Why Separate Backend & Worker?
- **Backend (FastAPI)**: Must respond to webhooks in < 10 seconds or GitHub retries
- **Worker (Celery)**: Can take 30+ seconds to do AI processing
- **Pattern**: Receive → Acknowledge → Process Async

#### The Message Queue Pattern
```
GitHub → FastAPI → Redis Queue → Celery Worker → Post Comment Back
         (instant)                  (slow AI work)
```

### 📝 Completed Sprint 0
- [x] Install Python dependencies (FastAPI, Celery, PyGithub, HuggingFace Hub)
- [x] Test FastAPI locally
- [x] Set up Docker Compose (Postgres + Redis)
- [x] Build webhook endpoint with signature verification
- [x] Set up Celery worker
- [x] Connect webhook to Celery task queue

### 🎯 Current Status
We have built the complete pipeline:
```
GitHub Webhook → FastAPI → Redis Queue → Celery Worker
```

### 📝 Completed Sprint 1 ✅
- [x] Test end-to-end flow
- [x] Integrate HuggingFace models for PR summarization
- [x] Parse PR diffs
- [x] Post comments back to GitHub
- [x] GitHub API integration (fetch PRs, post comments)
- [x] AI-powered summarization with fallbacks
- [x] PR classification (bug/feature/refactor/docs)
- [x] Risk detection and suggestions
- [x] Commit message generation

### 🎯 What We Built (Sprint 0 + Sprint 1)

**Complete Pipeline:**
```
GitHub Webhook → FastAPI → Redis → Celery Worker → AI Analysis → GitHub Comment
```

**Features:**
1. ✅ Webhook endpoint with HMAC signature verification
2. ✅ Async job processing with Celery + Redis
3. ✅ GitHub integration (fetch diffs, post comments)
4. ✅ HuggingFace AI integration (summarization, classification)
5. ✅ Smart fallbacks when AI is unavailable
6. ✅ Risk detection (large PRs, sensitive files)
7. ✅ Test/doc suggestions
8. ✅ Conventional commit message generation
9. ✅ Beautiful markdown comment formatting

**Tech Stack:**
- Backend: FastAPI, Python 3.13
- Worker: Celery, Redis
- Database: PostgreSQL (with pgvector for future)
- AI: HuggingFace Inference API
- Infrastructure: Docker Compose

### 📝 Next Steps (Future Sprints)
- [ ] Interactive commands (@PR-Pilot /review)
- [ ] Inline code suggestions
- [ ] Database models for storing analysis history
- [ ] User feedback collection
- [ ] Dashboard for viewing results
- [ ] Support for GitLab/BitBucket

---

## Questions & Answers

### Q: Why Redis instead of just calling the worker directly?
A: Redis provides:
1. **Buffering**: If 10 PRs open at once, queue them
2. **Reliability**: If worker crashes, jobs aren't lost
3. **Retry Logic**: Failed jobs can retry automatically
4. **Scaling**: Can add more workers to process faster

### Q: Could we use a single service instead of two?
A: Yes, but you'd hit GitHub's timeout limits. Separating concerns = better architecture.

---

*Keep adding notes as you learn! This becomes your personal reference.*

