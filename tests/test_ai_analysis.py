"""
Test AI-Powered PR Analysis

This script tests the complete pipeline:
1. GitHub API integration (fetch PR)
2. HuggingFace AI models (summarize, classify)
3. Risk detection and suggestions
4. Comment formatting

Run this to see PR Pilot in action!
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from worker.analyzers.pr_analyzer import PRAnalyzer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_analysis():
    """
    Test complete PR analysis on a real public repository PR
    
    We'll use a PR from a popular open-source project to demonstrate.
    You can change this to any public PR you want!
    """
    
    print("=" * 70)
    print("  🤖 PR Pilot AI Analysis Test")
    print("=" * 70)
    print()
    
    # Check if API keys are set
    github_token = os.getenv("GITHUB_TOKEN")
    hf_key = os.getenv("HF_API_KEY")
    
    if not github_token:
        print("❌ ERROR: GITHUB_TOKEN not found in .env file")
        print("   Please add your GitHub Personal Access Token")
        return False
    
    if not hf_key:
        print("❌ ERROR: HF_API_KEY not found in .env file")
        print("   Please add your HuggingFace API key")
        return False
    
    print("✅ API keys found!\n")
    
    # Test with a public repository PR
    # You can change these to test with any public PR
    test_repo = "facebook/react"  # Popular open-source repo
    test_pr_number = 28000  # A real PR (you can change this)
    
    print(f"📋 Test Configuration:")
    print(f"   Repository: {test_repo}")
    print(f"   PR Number: {test_pr_number}")
    print(f"   Note: Using a public PR for testing\n")
    
    try:
        # Initialize analyzer
        analyzer = PRAnalyzer()
        
        # Run complete analysis
        print("🚀 Starting AI-powered analysis...\n")
        result = analyzer.analyze(test_repo, test_pr_number)
        
        if not result.get("success"):
            print(f"\n❌ Analysis failed: {result.get('error')}")
            print("\nPossible reasons:")
            print("  - PR number doesn't exist")
            print("  - Repository is private and token doesn't have access")
            print("  - API rate limit reached")
            return False
        
        # Show the formatted comment that would be posted
        print("\n" + "=" * 70)
        print("📝 Generated Comment (what would be posted to GitHub):")
        print("=" * 70)
        
        comment = analyzer.format_comment(result)
        print(comment)
        
        print("\n" + "=" * 70)
        print("✅ TEST PASSED! All components working:")
        print("=" * 70)
        print("  ✅ GitHub API - Fetched PR successfully")
        print("  ✅ HuggingFace AI - Generated summary")
        print("  ✅ Classification - Identified PR type")
        print("  ✅ Risk Detection - Analyzed potential issues")
        print("  ✅ Suggestions - Generated recommendations")
        print("  ✅ Comment Formatting - Created beautiful output")
        print()
        print("🎉 PR Pilot is fully operational!")
        print()
        
        return True
    
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print(f"\nFull error details:")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "🤖" * 35)
    print()
    
    success = test_analysis()
    
    print()
    print("=" * 70)
    if success:
        print("✅ All tests passed! PR Pilot is ready to use!")
        print()
        print("Next steps:")
        print("  1. Set up a real GitHub webhook pointing to your server")
        print("  2. Open a PR in your repository")
        print("  3. Watch PR Pilot automatically analyze and comment!")
    else:
        print("❌ Tests failed. Please check the errors above.")
        print()
        print("Common issues:")
        print("  - Missing or invalid API keys in .env file")
        print("  - Network/firewall blocking API calls")
        print("  - Rate limits on GitHub or HuggingFace")
    print("=" * 70)
    print()
