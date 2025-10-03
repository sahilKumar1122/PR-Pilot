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

### 📝 Next Steps
- [ ] Install Python dependencies
- [ ] Test FastAPI locally
- [ ] Connect to Redis
- [ ] Build first webhook endpoint

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

