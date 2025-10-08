# Screenshot Checklist ✅

Quick checklist for creating demo screenshots.

## Priority Screenshots (Do These First!)

### 1. PR Comment Analysis ⭐⭐⭐ (MOST IMPORTANT)
- [ ] Create a test PR with 5-10 file changes
- [ ] Wait for PR Pilot to analyze and comment
- [ ] Take full-page screenshot of the comment
- [ ] Save as: `pr-comment-analysis.png`
- [ ] Check that it shows all sections clearly

**What it should show:**
- ✅ AI-generated summary
- ✅ PR classification (bug/feature/etc)
- ✅ Files changed list
- ✅ Risk warnings
- ✅ Test/docs suggestions

---

### 2. Docker Services Running ⭐⭐
- [ ] Run: `docker compose ps`
- [ ] Ensure all services show "running" or "healthy"
- [ ] Screenshot the terminal output
- [ ] Save as: `docker-compose-running.png`

**Terminal should show:**
```
NAME                   STATUS
prpilot-backend-1      Up (healthy)
prpilot-worker-1       Up
prpilot-postgres-1     Up (healthy)
prpilot-redis-1        Up (healthy)
```

---

### 3. GitHub Webhook Setup ⭐⭐
- [ ] Go to GitHub repo → Settings → Webhooks
- [ ] Click on your PR Pilot webhook
- [ ] Scroll to see "Recent Deliveries"
- [ ] Take screenshot showing green checkmarks
- [ ] Save as: `github-webhook-setup.png`

**Should show:**
- ✅ Webhook URL configured
- ✅ Content type: application/json
- ✅ Secret configured (hidden)
- ✅ Pull requests event selected
- ✅ Green checkmarks in Recent Deliveries

---

## Optional Screenshots

### 4. API Documentation ⭐
- [ ] Open http://localhost:8000/docs
- [ ] Expand the `/webhooks/github` endpoint
- [ ] Take screenshot
- [ ] Save as: `api-docs.png`

### 5. Real-World Example ⭐
- [ ] Use `tests/test_ai_analysis.py` on a public repo
- [ ] Screenshot the analysis output
- [ ] Save as: `real-world-example.png`

---

## Screenshot Quality Guidelines

### Technical Requirements
- **Format**: PNG
- **Width**: 1000-1200px (readable but not huge)
- **File size**: < 500KB each
- **Quality**: Clear, readable text

### Content Guidelines
- [ ] Blur/redact any personal information
- [ ] Blur/redact any sensitive tokens or secrets
- [ ] Use a clean browser theme (light mode preferred)
- [ ] Close unnecessary tabs/windows
- [ ] Remove notifications or alerts

### Tools
- **Windows**: Snipping Tool (Win + Shift + S)
- **Mac**: Screenshot (Cmd + Shift + 4)
- **Browser**: Full Page Screen Capture extension
- **Optimization**: TinyPNG.com (compress images)

---

## After Taking Screenshots

1. **Move files** to `assets/screenshots/` folder
2. **Name them** according to the guide
3. **Optimize** images (reduce file size if > 500KB)
4. **Test** that they display correctly:
   ```markdown
   ![Alt text](assets/screenshots/filename.png)
   ```

5. **Commit** to git:
   ```bash
   git add assets/
   git commit -m "docs: add demo screenshots"
   git push
   ```

---

## Quick Tips

💡 **Don't have time for all screenshots?**
- Just do #1 (PR Comment) - it's the most important!
- Others can be added later

💡 **Want to see examples?**
- Check out similar projects on GitHub
- Search "AI code review tools" for inspiration

💡 **Recording a GIF instead?**
- Use ScreenToGif (Windows) or Kap (Mac)
- Shows the PR comment appearing live
- Even better than static screenshots!

---

## Status

- [ ] Priority screenshots completed
- [ ] Optional screenshots completed
- [ ] All images optimized
- [ ] README updated with images
- [ ] Committed and pushed

**Estimated time**: 15-30 minutes for priority screenshots
