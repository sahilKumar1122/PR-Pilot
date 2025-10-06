"""
Test Script for GitHub Webhook

This simulates what GitHub sends when a PR is opened.
Run this to test your webhook endpoint without needing GitHub.

Usage:
  python tests/test_webhook.py
"""

import hashlib
import hmac
import json

import requests

# Your local server
WEBHOOK_URL = "http://localhost:8000/webhooks/github"

# Use the same secret as in your .env file (or empty for testing)
WEBHOOK_SECRET = ""  # Leave empty for now, we'll add it later

# This is what GitHub sends when a PR is opened
mock_payload = {
    "action": "opened",
    "number": 123,
    "pull_request": {
        "number": 123,
        "title": "Add new feature: Dark mode toggle",
        "body": "This PR adds a dark mode toggle to the settings page.",
        "user": {"login": "testuser"},
        "head": {"ref": "feature/dark-mode", "sha": "abc123def456"},
        "base": {"ref": "main"},
    },
    "repository": {
        "full_name": "myorg/myrepo",
        "name": "myrepo",
        "owner": {"login": "myorg"},
    },
}


def send_webhook():
    """Send a mock webhook request to our local server"""

    # Convert payload to JSON string
    payload_json = json.dumps(mock_payload)
    body = payload_json.encode()

    headers = {
        "Content-Type": "application/json",
        "X-GitHub-Event": "pull_request",
    }

    # If we have a secret, compute the signature
    if WEBHOOK_SECRET:
        mac = hmac.new(WEBHOOK_SECRET.encode(), msg=body, digestmod=hashlib.sha256)
        signature = "sha256=" + mac.hexdigest()
        headers["X-Hub-Signature-256"] = signature
        print(f"✅ Signature: {signature[:20]}...")
    else:
        print("⚠️  No secret configured, sending without signature")

    # Send the request
    print(f"\n📤 Sending webhook to {WEBHOOK_URL}")
    print(f"   PR: {mock_payload['repository']['full_name']}#{mock_payload['number']}")
    print(f"   Title: {mock_payload['pull_request']['title']}\n")

    try:
        response = requests.post(WEBHOOK_URL, data=body, headers=headers, timeout=10)

        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Body: {response.json()}\n")

        if response.status_code == 200:
            print("✅ SUCCESS! Webhook received and processed")
        else:
            print("❌ FAILED! Check the error above")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to server")
        print("   Make sure your FastAPI server is running:")
        print("   cd backend && uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ ERROR: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("  GitHub Webhook Test Script")
    print("=" * 60)
    send_webhook()
