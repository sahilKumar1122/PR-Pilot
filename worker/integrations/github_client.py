"""
GitHub API Client

This module handles all GitHub interactions:
1. Fetch PR details and diffs
2. Post comments to PRs
3. Get file contents and metadata

We use PyGithub library which provides a clean Python interface
to the GitHub REST API.
"""

import os
from typing import Optional, Dict, Any
from github import Github, GithubException


class GitHubClient:
    """
    Wrapper around PyGithub for PR operations
    
    Usage:
        client = GitHubClient(token="ghp_...")
        pr_data = client.get_pr_details("owner/repo", 123)
        client.post_comment("owner/repo", 123, "Great PR!")
    """
    
    def __init__(self, token: Optional[str] = None):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub Personal Access Token or App token
        """
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            print("⚠️  WARNING: GITHUB_TOKEN not set. API calls will fail.")
        
        self.github = Github(self.token)
    
    def get_pr_details(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Fetch comprehensive PR details
        
        Args:
            repo_name: Full repository name (e.g., "octocat/Hello-World")
            pr_number: Pull request number
        
        Returns:
            Dict containing:
                - title, body, author
                - diff (the actual code changes!)
                - files_changed (list of modified files)
                - additions, deletions (line counts)
                - labels, reviewers, etc.
        
        Example:
            data = client.get_pr_details("myorg/myrepo", 42)
            print(data['diff'])  # See the actual code changes
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            
            # Get the diff (patch format)
            # This shows what actually changed in the code
            diff = pr.get_files()
            diff_text = ""
            
            for file in diff:
                if file.patch:  # Some files don't have patches (binary, etc.)
                    diff_text += f"\n--- {file.filename} ---\n"
                    diff_text += file.patch
                    diff_text += "\n"
            
            return {
                "title": pr.title,
                "body": pr.body or "",
                "author": pr.user.login,
                "diff": diff_text,
                "files_changed": [f.filename for f in diff],
                "additions": pr.additions,
                "deletions": pr.deletions,
                "state": pr.state,
                "labels": [label.name for label in pr.labels],
                "url": pr.html_url,
                "base_branch": pr.base.ref,
                "head_branch": pr.head.ref,
            }
        
        except GithubException as e:
            print(f"❌ Failed to fetch PR details: {e}")
            return {"error": str(e)}
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return {"error": str(e)}
    
    def post_comment(
        self,
        repo_name: str,
        pr_number: int,
        comment: str
    ) -> bool:
        """
        Post a comment to a PR
        
        This is how we send our AI analysis back to GitHub!
        
        Args:
            repo_name: Full repository name
            pr_number: Pull request number
            comment: Markdown-formatted comment text
        
        Returns:
            True if successful, False otherwise
        
        Example:
            success = client.post_comment(
                "myorg/myrepo",
                42,
                "## AI Analysis\\n\\nThis PR looks great! ✅"
            )
        """
        try:
            repo = self.github.get_repo(repo_name)
            pr = repo.get_pull(pr_number)
            pr.create_issue_comment(comment)
            
            print(f"✅ Posted comment to {repo_name}#{pr_number}")
            return True
        
        except GithubException as e:
            print(f"❌ Failed to post comment: {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def get_rate_limit(self) -> Dict[str, int]:
        """
        Check GitHub API rate limits
        
        GitHub has rate limits:
        - 5000 requests/hour for authenticated requests
        - 60 requests/hour for unauthenticated
        
        Returns:
            Dict with 'remaining' and 'limit' keys
        """
        try:
            rate_limit = self.github.get_rate_limit()
            return {
                "remaining": rate_limit.core.remaining,
                "limit": rate_limit.core.limit,
                "reset_time": rate_limit.core.reset.isoformat()
            }
        except Exception as e:
            print(f"❌ Failed to get rate limit: {e}")
            return {"remaining": 0, "limit": 0, "reset_time": "unknown"}


# Singleton instance
_github_client_instance = None

def get_github_client() -> GitHubClient:
    """Get a singleton GitHub client instance"""
    global _github_client_instance
    if _github_client_instance is None:
        _github_client_instance = GitHubClient()
    return _github_client_instance
