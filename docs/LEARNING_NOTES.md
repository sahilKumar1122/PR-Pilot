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

### 📝 Next Steps
- [ ] Test end-to-end flow
- [ ] Integrate HuggingFace models for PR summarization
- [ ] Parse PR diffs
- [ ] Post comments back to GitHub

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

