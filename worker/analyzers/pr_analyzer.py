"""
PR Analyzer

This is the brain of PR Pilot!
It orchestrates the entire analysis pipeline:
1. Fetch PR data from GitHub
2. Analyze with AI
3. Generate suggestions
4. Format and post comment

Think of this as the "conductor" that coordinates all the pieces.
"""

from typing import Dict, Any
from worker.integrations.github_client import get_github_client
from worker.integrations.huggingface_client import get_hf_client


class PRAnalyzer:
    """
    Main PR analysis engine
    
    Usage:
        analyzer = PRAnalyzer()
        result = analyzer.analyze("owner/repo", 123)
        # Returns comprehensive analysis dict
    """
    
    def __init__(self):
        self.github = get_github_client()
        self.hf = get_hf_client()
    
    def analyze(self, repo_name: str, pr_number: int) -> Dict[str, Any]:
        """
        Complete PR analysis pipeline
        
        Steps:
        1. Fetch PR details and diff from GitHub
        2. Summarize changes using AI
        3. Classify PR intent
        4. Generate commit message
        5. Detect potential issues
        6. Suggest tests/docs if needed
        
        Args:
            repo_name: Repository (e.g., "octocat/Hello-World")
            pr_number: PR number
        
        Returns:
            Analysis results dict
        """
        print(f"\n{'='*60}")
        print(f"🔍 Analyzing {repo_name}#{pr_number}")
        print(f"{'='*60}\n")
        
        # Step 1: Fetch PR data
        print("📥 Step 1: Fetching PR details from GitHub...")
        pr_data = self.github.get_pr_details(repo_name, pr_number)
        
        if "error" in pr_data:
            return {
                "success": False,
                "error": pr_data["error"]
            }
        
        print(f"   ✅ Found PR: {pr_data['title']}")
        print(f"   📝 Author: {pr_data['author']}")
        print(f"   📊 Changes: +{pr_data['additions']} -{pr_data['deletions']} lines")
        print(f"   📁 Files: {len(pr_data['files_changed'])} changed\n")
        
        # Step 2: Generate summary
        print("🤖 Step 2: AI Summarization...")
        summary_text = self._create_summary_input(pr_data)
        summary = self.hf.summarize(summary_text)
        print(f"   ✅ Summary: {summary}\n")
        
        # Step 3: Classify PR type
        print("🏷️  Step 3: PR Classification...")
        classification_text = f"{pr_data['title']}. {pr_data['body'][:200]}"
        labels = ["bug", "feature", "refactor", "docs"]
        classification = self.hf.classify(classification_text, labels)
        
        # Get the top classification
        pr_type = max(classification, key=classification.get)
        confidence = classification[pr_type]
        print(f"   ✅ Type: {pr_type} (confidence: {confidence:.0%})\n")
        
        # Step 4: Generate commit message
        print("💬 Step 4: Generating commit message...")
        commit_msg = self.hf.generate_commit_message(
            pr_data['title'],
            summary,
            pr_type
        )
        print(f"   ✅ Suggested: {commit_msg}\n")
        
        # Step 5: Detect potential issues
        print("⚠️  Step 5: Detecting potential issues...")
        risks = self._detect_risks(pr_data)
        if risks:
            for risk in risks:
                print(f"   - {risk}")
        else:
            print("   ✅ No major risks detected")
        print()
        
        # Step 6: Check for missing tests/docs
        print("🧪 Step 6: Checking tests & documentation...")
        suggestions = self._generate_suggestions(pr_data)
        for suggestion in suggestions:
            print(f"   - {suggestion}")
        print()
        
        # Compile results
        result = {
            "success": True,
            "pr_data": {
                "title": pr_data['title'],
                "author": pr_data['author'],
                "url": pr_data['url'],
                "additions": pr_data['additions'],
                "deletions": pr_data['deletions'],
                "files_changed": pr_data['files_changed'],
            },
            "analysis": {
                "summary": summary,
                "type": pr_type,
                "confidence": confidence,
                "classification_scores": classification,
            },
            "suggestions": {
                "commit_message": commit_msg,
                "risks": risks,
                "improvements": suggestions,
            }
        }
        
        print(f"{'='*60}")
        print(f"✅ Analysis complete!")
        print(f"{'='*60}\n")
        
        return result
    
    def _create_summary_input(self, pr_data: Dict) -> str:
        """
        Create input text for summarization
        
        Combines title, description, and a preview of changes
        """
        text = f"Title: {pr_data['title']}\n\n"
        
        if pr_data['body']:
            text += f"Description: {pr_data['body'][:300]}\n\n"
        
        text += f"Changed files: {', '.join(pr_data['files_changed'][:5])}\n\n"
        
        # Add a preview of the diff (first 500 chars)
        if pr_data['diff']:
            text += f"Changes preview:\n{pr_data['diff'][:500]}"
        
        return text
    
    def _detect_risks(self, pr_data: Dict) -> list:
        """
        Detect potential risks based on heuristics
        
        These are simple rules - you can make them smarter!
        """
        risks = []
        
        # Large PRs are risky
        total_changes = pr_data['additions'] + pr_data['deletions']
        if total_changes > 500:
            risks.append("⚠️  Large PR (500+ lines): Consider splitting into smaller PRs")
        
        # Many files changed
        if len(pr_data['files_changed']) > 10:
            risks.append("⚠️  Many files changed: Review carefully for side effects")
        
        # Check for sensitive files
        sensitive_patterns = ['config', 'secret', 'password', 'key', 'token', '.env']
        for file in pr_data['files_changed']:
            if any(pattern in file.lower() for pattern in sensitive_patterns):
                risks.append(f"🔒 Sensitive file modified: {file}")
                break
        
        return risks
    
    def _generate_suggestions(self, pr_data: Dict) -> list:
        """
        Generate improvement suggestions
        
        Checks for missing tests, docs, etc.
        """
        suggestions = []
        
        # Check for test files
        has_tests = any(
            'test' in f.lower() or 'spec' in f.lower() 
            for f in pr_data['files_changed']
        )
        
        has_source_code = any(
            f.endswith(('.py', '.js', '.ts', '.java', '.go'))
            and 'test' not in f.lower()
            for f in pr_data['files_changed']
        )
        
        if has_source_code and not has_tests:
            suggestions.append("🧪 Consider adding tests for the new code")
        
        # Check for documentation
        has_docs = any(
            f.endswith(('.md', '.rst', '.txt')) or 'doc' in f.lower()
            for f in pr_data['files_changed']
        )
        
        if not has_docs and len(pr_data['files_changed']) > 3:
            suggestions.append("📚 Consider updating documentation")
        
        if not suggestions:
            suggestions.append("✅ Looks good!")
        
        return suggestions
    
    def format_comment(self, analysis: Dict[str, Any]) -> str:
        """
        Format analysis results as a beautiful GitHub comment
        
        Uses Markdown for nice formatting
        """
        if not analysis.get("success"):
            return f"❌ **Analysis Failed**\n\n{analysis.get('error', 'Unknown error')}"
        
        pr = analysis['pr_data']
        ai = analysis['analysis']
        suggestions = analysis['suggestions']
        
        comment = f"""## 🤖 PR Pilot Analysis

**Summary:** {ai['summary']}

### 📊 PR Details
- **Type:** `{ai['type']}` (confidence: {ai['confidence']:.0%})
- **Changes:** +{pr['additions']} -{pr['deletions']} lines across {len(pr['files_changed'])} files
- **Author:** @{pr['author']}

### 💬 Suggested Commit Message
```
{suggestions['commit_message']}
```

### ⚠️  Potential Risks
"""
        
        if suggestions['risks']:
            for risk in suggestions['risks']:
                comment += f"- {risk}\n"
        else:
            comment += "- ✅ No major risks detected\n"
        
        comment += "\n### 💡 Suggestions\n"
        for suggestion in suggestions['improvements']:
            comment += f"- {suggestion}\n"
        
        comment += f"""
---
<sub>🤖 Generated by [PR Pilot](https://github.com/sahilKumar1122/PR-Pilot) • Powered by AI</sub>
"""
        
        return comment
