"""
FastAPI Application Entry Point

This is the web server that:
1. Receives webhook events from GitHub
2. Validates the webhook signature (security!)
3. Quickly enqueues a job for the worker
4. Returns 200 OK to GitHub (must be fast < 10s)

Why FastAPI?
- Fast & async (handles many webhooks concurrently)
- Automatic API docs (visit /docs when running)
- Type hints make code safer
"""

import hmac
import hashlib
import os
import sys
from typing import Optional

from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv

# Add worker directory to Python path so we can import tasks
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from worker.tasks import analyze_pr

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="PR Pilot API",
    description="AI-powered PR review webhook receiver",
    version="0.1.0"
)

# Get the webhook secret from environment
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pr-pilot"}


@app.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None)
):
    """
    GitHub Webhook Endpoint
    
    This receives events from GitHub when PRs are opened/updated.
    
    Security: GitHub signs each request with HMAC-SHA256
    We verify the signature to ensure it's really from GitHub.
    
    Flow:
    1. Read the raw request body
    2. Verify GitHub's signature
    3. Parse the JSON payload
    4. Filter for PR events we care about
    5. Enqueue job for worker (TODO)
    6. Return 200 OK quickly
    """
    
    # Step 1: Read raw body (needed for signature verification)
    body = await request.body()
    
    # Step 2: Verify signature (CRITICAL for security!)
    if GITHUB_WEBHOOK_SECRET:
        if not x_hub_signature_256:
            raise HTTPException(
                status_code=401, 
                detail="Missing signature header"
            )
        
        # GitHub sends: "sha256=<hash>"
        # We need to compute the same hash and compare
        mac = hmac.new(
            GITHUB_WEBHOOK_SECRET.encode(),
            msg=body,
            digestmod=hashlib.sha256
        )
        expected_signature = "sha256=" + mac.hexdigest()
        
        # Use constant-time comparison to prevent timing attacks
        if not hmac.compare_digest(expected_signature, x_hub_signature_256):
            raise HTTPException(
                status_code=401,
                detail="Invalid signature"
            )
    else:
        # WARNING: No secret configured! Only for local testing
        print("⚠️  WARNING: GITHUB_WEBHOOK_SECRET not set. Skipping verification.")
    
    # Step 3: Parse JSON payload
    payload = await request.json()
    
    # Step 4: Filter events
    action = payload.get("action")
    
    # We only care about these PR actions
    if action in {"opened", "synchronize", "reopened"}:
        pr = payload.get("pull_request", {})
        repo_full_name = payload.get("repository", {}).get("full_name")
        pr_number = pr.get("number")
        pr_title = pr.get("title")
        
        print(f"📥 Received PR event: {repo_full_name}#{pr_number} - {pr_title}")
        print(f"   Action: {action}")
        
        # Enqueue Celery job for background processing
        task = analyze_pr.delay(repo_full_name, pr_number, payload)
        
        print(f"   Task ID: {task.id}")
        
        return {
            "status": "enqueued",
            "repo": repo_full_name,
            "pr_number": pr_number,
            "action": action,
            "task_id": task.id
        }
    
    # Other events (like PR closed, comments) - we ignore for now
    return {"status": "ignored", "action": action}

