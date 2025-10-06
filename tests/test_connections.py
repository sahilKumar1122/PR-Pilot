"""
Test Database and Redis Connections

Quick script to verify Docker services are accessible.
"""

import os
import sys


# Test Redis Connection
def test_redis():
    try:
        import redis

        r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        r.ping()
        print("[OK] Redis: Connected successfully!")
        r.set("test_key", "Hello from PR-Pilot!")
        value = r.get("test_key")
        print(f"   - Test read/write: '{value}'")
        r.delete("test_key")
        return True
    except Exception as e:
        print(f"[FAIL] Redis: Failed - {e}")
        return False


# Test PostgreSQL Connection
def test_postgres():
    try:
        import psycopg

        conn = psycopg.connect(
            "postgresql://prpilot:devpassword@127.0.0.1:5432/prpilot", connect_timeout=3
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print("[OK] PostgreSQL: Connected successfully!")
        print(f"   - Version: {version[:50]}...")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"[FAIL] PostgreSQL: Failed - {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Docker Services")
    print("=" * 60)
    print()

    redis_ok = test_redis()
    print()
    postgres_ok = test_postgres()
    print()

    if redis_ok and postgres_ok:
        print("[SUCCESS] All services are ready!")
        sys.exit(0)
    else:
        print("[FAIL] Some services failed. Check Docker containers:")
        print("   docker-compose ps")
        sys.exit(1)
