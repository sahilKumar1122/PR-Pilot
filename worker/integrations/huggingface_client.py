"""
HuggingFace API Client

This module provides a clean interface to HuggingFace's Inference API.
We use it for:
1. Summarization - Turn code diffs into human-readable summaries
2. Zero-shot classification - Categorize PRs (bug/feature/refactor/docs)
3. Text generation - Generate commit messages and suggestions

Why HuggingFace?
- Free tier available
- Open source models
- No vendor lock-in
- Great for learning AI integration
"""

import os
from typing import Dict, List, Optional
from huggingface_hub import InferenceClient


class HuggingFaceClient:
    """
    Wrapper around HuggingFace Inference API
    
    Usage:
        client = HuggingFaceClient(api_key="your_key")
        summary = client.summarize("Long text here...")
        category = client.classify("PR description", ["bug", "feature"])
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the HF client
        
        Args:
            api_key: HuggingFace API token. If None, reads from env.
        """
        self.api_key = api_key or os.getenv("HF_API_KEY")
        if not self.api_key:
            print("⚠️  WARNING: HF_API_KEY not set. API calls will fail.")
        
        # For corporate networks with SSL inspection
        # This disables SSL verification (use only in development!)
        import ssl
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        self.client = InferenceClient(token=self.api_key)
        
        # Monkey patch to disable SSL verification
        import requests
        original_request = requests.Session.request
        def patched_request(self, method, url, **kwargs):
            kwargs['verify'] = False
            return original_request(self, method, url, **kwargs)
        requests.Session.request = patched_request
    
    def summarize(
        self, 
        text: str, 
        max_length: int = 150,
        min_length: int = 30
    ) -> str:
        """
        Summarize text using a lightweight model
        
        We use distilbart which is faster and more reliable for free tier.
        
        Args:
            text: Text to summarize (PR diff, description, etc.)
            max_length: Maximum summary length in tokens
            min_length: Minimum summary length in tokens
        
        Returns:
            Summarized text
        
        Example:
            summary = client.summarize('''
                Added new authentication middleware
                Updated user login flow
                Fixed session timeout bug
            ''')
            # Returns: "This PR adds authentication middleware and fixes login issues"
        """
        # Try multiple times with different strategies
        models_to_try = [
            "sshleifer/distilbart-cnn-12-6",  # Lighter, faster model
            "facebook/bart-large-cnn",  # Original model
        ]
        
        for model in models_to_try:
            try:
                # Truncate if text is too long (model has limits)
                if len(text) > 512:
                    text = text[:512] + "..."
                
                print(f"   Trying model: {model}...")
                
                import time
                start = time.time()
                
                result = self.client.summarization(
                    text,
                    model=model
                )
                
                elapsed = time.time() - start
                print(f"   ✅ Success in {elapsed:.1f}s")
                
                # Handle different response formats
                if isinstance(result, str):
                    return result
                elif hasattr(result, 'summary_text'):
                    return result.summary_text
                elif isinstance(result, dict) and 'summary_text' in result:
                    return result['summary_text']
                elif isinstance(result, list) and len(result) > 0:
                    if isinstance(result[0], dict) and 'summary_text' in result[0]:
                        return result[0]['summary_text']
                    return str(result[0])
                else:
                    return str(result)
            
            except Exception as e:
                print(f"   ⚠️  Model {model} failed: {str(e)[:100]}")
                continue
        
        # If all models fail, create a simple summary
        print("   ℹ️  Using fallback: Simple text extraction")
        return self._fallback_summary(text)
    
    def _fallback_summary(self, text: str) -> str:
        """
        Simple fallback when AI models fail
        Just extract the first meaningful sentence
        """
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines:
            # Try to find title/description
            for line in lines[:5]:
                if len(line) > 20 and not line.startswith(('---', '+++', '@@')):
                    return line[:200]
        return "Unable to generate AI summary (see PR details below)"
    
    def classify(
        self,
        text: str,
        labels: List[str]
    ) -> Dict[str, float]:
        """
        Classify text into categories using zero-shot classification
        
        Zero-shot means the model wasn't specifically trained on these labels,
        but it can still understand and classify them! Pretty cool!
        
        Args:
            text: Text to classify (PR title + description)
            labels: List of possible categories
        
        Returns:
            Dict mapping label to confidence score
        
        Example:
            result = client.classify(
                "Fix memory leak in cache module",
                ["bug", "feature", "refactor", "docs"]
            )
            # Returns: {"bug": 0.95, "feature": 0.03, "refactor": 0.02, ...}
        """
        try:
            # Truncate long text
            if len(text) > 512:
                text = text[:512]
            
            print(f"   Classifying with zero-shot model...")
            
            result = self.client.zero_shot_classification(
                text,
                labels=labels,
                model="facebook/bart-large-mnli"
            )
            
            print(f"   ✅ Classification complete")
            
            # Handle different response formats
            if isinstance(result, dict):
                if 'labels' in result and 'scores' in result:
                    return {
                        label: score 
                        for label, score in zip(result['labels'], result['scores'])
                    }
            elif hasattr(result, 'labels') and hasattr(result, 'scores'):
                return {
                    label: score 
                    for label, score in zip(result.labels, result.scores)
                }
            elif isinstance(result, list) and len(result) > 0:
                # Sometimes returns list of dicts
                item = result[0]
                if isinstance(item, dict) and 'labels' in item and 'scores' in item:
                    return {
                        label: score 
                        for label, score in zip(item['labels'], item['scores'])
                    }
            
            # If we can't parse it, fall back
            print(f"   ⚠️  Unexpected response format: {type(result)}")
            raise ValueError("Unexpected response format")
        
        except Exception as e:
            print(f"   ⚠️  Classification failed: {str(e)[:100]}")
            print(f"   ℹ️  Using fallback: Keyword-based classification")
            return self._fallback_classify(text, labels)
    
    def _fallback_classify(self, text: str, labels: List[str]) -> Dict[str, float]:
        """
        Simple keyword-based classification fallback
        """
        text_lower = text.lower()
        
        # Simple keyword matching
        scores = {}
        keywords = {
            "bug": ["fix", "bug", "issue", "error", "crash", "broken"],
            "feature": ["add", "new", "feature", "implement", "create"],
            "refactor": ["refactor", "cleanup", "improve", "optimize", "reorganize"],
            "docs": ["doc", "readme", "comment", "documentation"]
        }
        
        for label in labels:
            if label in keywords:
                matches = sum(1 for kw in keywords[label] if kw in text_lower)
                scores[label] = min(matches * 0.25, 0.9)  # Cap at 0.9
            else:
                scores[label] = 0.1
        
        # Normalize to sum to 1.0
        total = sum(scores.values()) or 1.0
        return {k: v/total for k, v in scores.items()}
    
    def generate_commit_message(
        self,
        pr_title: str,
        summary: str,
        pr_type: str
    ) -> str:
        """
        Generate a Conventional Commits style message
        
        Format: <type>(<scope>): <description>
        Example: feat(auth): add OAuth2 authentication
        
        For now, we'll use a template approach.
        Later, we can use a generative model if needed.
        
        Args:
            pr_title: PR title
            summary: PR summary
            pr_type: Classification (bug/feature/etc)
        
        Returns:
            Conventional commit message
        """
        # Map our classifications to conventional commit types
        type_mapping = {
            "bug": "fix",
            "feature": "feat",
            "refactor": "refactor",
            "docs": "docs"
        }
        
        commit_type = type_mapping.get(pr_type, "chore")
        
        # Simple template for now
        # TODO: Use a generative model for more sophisticated messages
        return f"{commit_type}: {pr_title.lower()}"


# Singleton instance for reuse
_client_instance = None

def get_hf_client() -> HuggingFaceClient:
    """
    Get a singleton HuggingFace client instance
    
    This avoids creating multiple clients and reuses connections.
    """
    global _client_instance
    if _client_instance is None:
        _client_instance = HuggingFaceClient()
    return _client_instance
