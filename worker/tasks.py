"""
Celery Tasks for PR Analysis

This is where the REAL work happens:
1. Fetch PR diff from GitHub API
2. Parse the diff (what files changed?)
3. Call AI models (summarization, classification)
4. Generate suggestions (commit message, tests)
5. Post comment back to GitHub

Why Celery?
- Handles long-running tasks (30+ seconds)
- Can retry failed tasks automatically
- Can scale workers horizontally
- Won't block the webhook endpoint
"""

from celery import Celery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our analyzer and clients
from worker.analyzers.pr_analyzer import PRAnalyzer
from worker.integrations.github_client import get_github_client

# Connect to Redis (our message queue)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("pr-pilot", broker=redis_url, backend=redis_url)

@celery_app.task(bind=True, max_retries=3)
def analyze_pr(self, repo: str, pr_number: int, payload: dict):
    """
    Main task that analyzes a pull request.
    
    This is the complete pipeline:
    1. Fetch PR from GitHub
    2. Analyze with AI (summarize, classify)
    3. Generate suggestions
    4. Post comment back to GitHub
    
    Args:
        repo: Repository full name (e.g., "owner/repo-name")
        pr_number: PR number
        payload: Full webhook payload from GitHub
    
    Returns:
        dict with analysis results
    """
    try:
        print(f"\n🚀 Starting analysis for {repo}#{pr_number}")
        
        # Initialize analyzer
        analyzer = PRAnalyzer()
        github = get_github_client()
        
        # Step 1-6: Comprehensive analysis
        analysis = analyzer.analyze(repo, pr_number)
        
        if not analysis.get("success"):
            print(f"❌ Analysis failed: {analysis.get('error')}")
            return {
                "status": "failed",
                "error": analysis.get('error')
            }
        
        # Step 7: Format comment
        print("📝 Formatting GitHub comment...")
        comment = analyzer.format_comment(analysis)
        
        # Step 8: Post to GitHub
        print("📤 Posting comment to GitHub...")
        success = github.post_comment(repo, pr_number, comment)
        
        if success:
            print(f"✅ Successfully analyzed and commented on {repo}#{pr_number}\n")
            return {
                "status": "success",
                "analysis": analysis,
                "commented": True
            }
        else:
            print(f"⚠️  Analysis succeeded but comment failed for {repo}#{pr_number}\n")
            return {
                "status": "partial_success",
                "analysis": analysis,
                "commented": False
            }
    
    except Exception as e:
        print(f"❌ Task failed with error: {e}")
        
        # Retry logic
        if self.request.retries < self.max_retries:
            print(f"   Retrying... (attempt {self.request.retries + 1}/{self.max_retries})")
            raise self.retry(exc=e, countdown=60)  # Retry after 60 seconds
        
        return {
            "status": "error",
            "error": str(e)
        }

