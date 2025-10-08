# Demo Content Creation Guide

This guide will help you create professional screenshots and a demo video for PR Pilot.

## 📸 Screenshots Needed

### 1. PR Analysis Comment (Most Important!)

**What to capture:**
- A GitHub PR with PR Pilot's analysis comment
- Should show all sections: Summary, Classification, Files Changed, Risks, Suggestions

**How to capture:**
1. Create a test repository
2. Make a PR with meaningful changes (e.g., add a feature with 5-10 files)
3. Let PR Pilot analyze it
4. Take a full-page screenshot of the comment

**Tools:**
- Chrome/Edge: Full page screenshot extension
- Windows: Snipping Tool or Win+Shift+S
- Mac: Cmd+Shift+4

**Save as:** `assets/screenshots/pr-comment-analysis.png`

---

### 2. GitHub Webhook Configuration

**What to capture:**
- GitHub repo Settings → Webhooks page
- Your PR Pilot webhook configured and showing green checkmark

**How to capture:**
1. Go to your repo → Settings → Webhooks
2. Click on your PR Pilot webhook
3. Screenshot showing:
   - Payload URL
   - Content type: application/json
   - Secret: [configured]
   - Events: Pull requests
   - Active: ✅
   - Recent Deliveries with green checkmarks

**Save as:** `assets/screenshots/github-webhook-setup.png`

---

### 3. Docker Compose Running

**What to capture:**
- Terminal showing `docker compose ps` with all services healthy
- Clean, professional terminal theme

**How to capture:**
```bash
# Make terminal look nice
docker compose ps

# Should show:
# - postgres (healthy)
# - redis (healthy)  
# - backend (healthy)
# - worker (running)
```

**Save as:** `assets/screenshots/docker-compose-running.png`

---

### 4. API Documentation Page

**What to capture:**
- FastAPI's auto-generated docs at http://localhost:8000/docs
- Shows all endpoints beautifully

**How to capture:**
1. Start backend: `docker compose up -d`
2. Open: http://localhost:8000/docs
3. Expand the webhook endpoint to show details
4. Take screenshot

**Save as:** `assets/screenshots/api-docs.png`

---

### 5. Real-World Example (Optional but Impressive)

**What to capture:**
- PR Pilot analyzing a real PR from a popular open source project
- Shows it works on real codebases

**How to capture:**
1. Use the test script with a public repo
2. Screenshot the resulting analysis

**Save as:** `assets/screenshots/real-world-example.png`

---

## 🎥 Demo Video Script

### Video Structure (3-5 minutes)

**Intro (30 seconds)**
```
[Screen: PR Pilot logo/README]

"Hi! I'm going to show you PR Pilot - an AI-powered pull request reviewer 
that automatically analyzes your code changes.

Unlike other tools, PR Pilot is:
- Self-hosted (your code stays private)
- Uses free HuggingFace models (no OpenAI costs)
- Works with smart fallbacks (always reliable)

Let's see it in action!"
```

**Part 1: Setup (60 seconds)**
```
[Screen: Terminal]

"Setting up PR Pilot is simple. Just three steps:

1. Clone the repository
   [Type: git clone https://github.com/sahilKumar1122/PR-Pilot.git]
   
2. Configure your environment
   [Show: cp env.example .env]
   [Show: editing .env with tokens]
   
3. Start with Docker
   [Type: docker compose up -d]
   [Show: Services starting]

And we're ready!"
```

**Part 2: GitHub Webhook Configuration (45 seconds)**
```
[Screen: GitHub repository settings]

"Now let's connect it to GitHub.

1. Go to your repo Settings → Webhooks → Add webhook
   
2. Enter your PR Pilot URL
   [Type: https://your-domain.com/webhooks/github]
   
3. Set content type to JSON
   [Click: application/json]
   
4. Add your webhook secret
   [Type: ********]
   
5. Select 'Pull requests' events
   [Click checkbox]
   
6. Save!
   [Click: Add webhook]

Perfect! Green checkmark means we're connected."
```

**Part 3: Live Demo (90 seconds)**
```
[Screen: GitHub - Creating a PR]

"Let's see it work. I'll create a pull request with some code changes.

[Create a branch]
[Make meaningful changes - add a feature]
[Commit and push]
[Open pull request]

And... within seconds, PR Pilot is already analyzing!

[Switch to terminal showing logs]

Look at what's happening:
- Fetching the PR diff from GitHub
- Running AI summarization
- Detecting risks
- Generating suggestions

[Switch back to GitHub PR]

And there it is! PR Pilot has posted a comprehensive analysis:

1. AI-generated summary - explains what this PR does
2. Classification - correctly identified this as a 'feature'
3. Files changed - lists all modified files
4. Risk assessment - flags potential concerns
5. Suggestions - recommends tests and documentation

All automatically, in under 60 seconds!"
```

**Part 4: Features Highlight (45 seconds)**
```
[Screen: Split screen showing different PR types]

"PR Pilot handles all types of PRs:

- Bug fixes [Show example]
- New features [Show example]
- Refactoring [Show example]
- Documentation [Show example]

It even has smart fallbacks - if AI models are slow or timeout,
it uses keyword-based analysis to ensure you always get results.

[Show: Architecture diagram from README]

The architecture is simple but powerful:
- FastAPI backend receives webhooks instantly
- Celery workers process analysis in background
- Redis handles the queue
- Everything runs in Docker containers"
```

**Outro (30 seconds)**
```
[Screen: README with badges and links]

"PR Pilot is open source, well-documented, and ready for production.

Check out:
- Complete API documentation
- Deployment guides for Docker and Cloud platforms
- Troubleshooting guide for common issues

Star the repo, try it out, and let me know what you think!

Links in the description. Thanks for watching!"

[End screen with:
- GitHub repo link
- Documentation links
- Your contact/social media]
```

---

## 🎬 Recording Tools

### Screen Recording
- **Windows**: OBS Studio (free), Camtasia (paid)
- **Mac**: QuickTime, ScreenFlow
- **Cross-platform**: OBS Studio, Loom

### Video Editing
- **Simple**: iMovie (Mac), Clipchamp (Windows)
- **Advanced**: DaVinci Resolve (free), Adobe Premiere

### Recording Tips
1. **Clean desktop**: Hide personal info, close unnecessary windows
2. **Good resolution**: 1920x1080 minimum
3. **Clear audio**: Use a decent microphone or clear voice
4. **Pacing**: Speak slowly and clearly
5. **Smooth cursor**: Don't move mouse too fast
6. **Rehearse**: Practice the demo 2-3 times first
7. **Short takes**: Record in segments, then edit together

---

## 📝 Video Description Template

```
🤖 PR Pilot - AI-Powered Pull Request Reviews

Automatically analyze GitHub pull requests with AI:
✅ Smart summaries using HuggingFace models
✅ Risk detection and security alerts
✅ Test & documentation suggestions
✅ Self-hosted (your code stays private)
✅ Free to use (no OpenAI API costs)

⏱️ Timestamps:
0:00 - Introduction
0:30 - Quick Setup
1:30 - GitHub Webhook Configuration
2:15 - Live Demo
3:45 - Features Overview
4:30 - Get Started

🔗 Links:
GitHub: https://github.com/sahilKumar1122/PR-Pilot
Docs: https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/
API Reference: https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/API.md
Deploy Guide: https://github.com/sahilKumar1122/PR-Pilot/blob/main/docs/DEPLOYMENT.md

💬 Questions? Open an issue or discussion on GitHub!

#OpenSource #AI #GitHub #CodeReview #Python #FastAPI #DevTools
```

---

## 🎨 Thumbnail Ideas

**Option 1: Before/After**
```
[Left side] Manual PR review (person looking tired)
[Right side] PR Pilot logo + "Automated!"
[Bottom] "PR Pilot - AI Code Reviews"
```

**Option 2: Tech Stack**
```
[Center] PR Pilot logo
[Around it] Icons: GitHub, Python, Docker, AI
[Bottom] "Open Source • AI-Powered • Self-Hosted"
```

**Option 3: Screenshot**
```
[Background] Blurred PR comment screenshot
[Center] "PR Pilot" in large text
[Bottom] "Automated PR Reviews with AI"
```

**Tools for Thumbnails:**
- Canva (easiest, templates available)
- Figma (more control)
- Photoshop (professional)

---

## 📤 Where to Upload

### Video Hosting
1. **YouTube** (recommended)
   - Embed in README
   - SEO benefits
   - Professional

2. **Loom**
   - Quick and easy
   - Direct links
   - Good for docs

3. **GitHub Assets**
   - Keep everything in repo
   - May have size limits
   - Less discoverable

### After Uploading

Update README.md:
```markdown
## 🎥 Demo

Watch PR Pilot in action:

[![PR Pilot Demo](assets/screenshots/thumbnail.png)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

Or view [screenshots](assets/screenshots/) of key features.
```

---

## ✅ Checklist

Before you start recording:

- [ ] Clean test environment set up
- [ ] Docker services running smoothly
- [ ] Test PR ready to demonstrate
- [ ] GitHub webhook configured
- [ ] Desktop cleaned up (no personal info)
- [ ] Good internet connection (for live demo)
- [ ] Script/notes prepared
- [ ] Recording software tested
- [ ] Microphone tested (if using voice)
- [ ] 30 minutes blocked for recording

After recording:

- [ ] Edit video (trim, add captions if needed)
- [ ] Create thumbnail
- [ ] Write description with links
- [ ] Add timestamps
- [ ] Upload to YouTube/platform
- [ ] Update README with embed
- [ ] Add screenshots to README
- [ ] Commit and push to GitHub

---

## 🚀 Quick Demo (No Recording)

If you don't want to record a video right now, create a quick animated GIF:

**Using Terminalizer:**
```bash
npm install -g terminalizer

# Record
terminalizer record demo

# In the terminal:
# - Show docker compose up
# - Show curl to webhook
# - Show logs
# Exit: Ctrl+D

# Generate GIF
terminalizer generate demo
```

**Or use ScreenToGif** (Windows):
- Record just the PR comment appearing
- Export as GIF
- Much quicker than full video!

---

## 📸 Screenshot Naming Convention

```
pr-comment-analysis.png          # Main screenshot
pr-comment-analysis-dark.png     # Dark mode version
github-webhook-setup.png         # Webhook configuration
docker-compose-running.png       # Services running
api-docs.png                     # FastAPI docs
architecture-diagram.png         # System architecture
real-world-example.png          # Production usage
```

---

Good luck! Take your time to create quality content - it's worth it! 🎬✨
