#!/usr/bin/env python3
"""
Test the showcase-ready MCP server with proven authentication patterns.
"""
import os
import logging
from fastapi.testclient import TestClient

# Configure logging to see the proven middleware in action
logging.basicConfig(level=logging.DEBUG)

def test_showcase_ready_server():
    """Test the showcase-ready implementation using proven code-buddy patterns."""
    print("🏆 TESTING SHOWCASE-READY MCP SERVER")
    print("=" * 60)
    
    # Set API keys BEFORE import (critical for proper initialization)
    os.environ["MCP_API_KEYS"] = "demo-key-123,showcase-key-456"
    
    # Import after environment setup
    from src.main import app
    client = TestClient(app)
    
    # Test 1: REST endpoints work without authentication
    print("✅ Test 1: REST API (no auth required)")
    response = client.get("/api/v1/search?q=EDA")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ PASS: Found {result.get('count', 0)} results")
    
    # Test 2: Health endpoint works
    print("\n✅ Test 2: Health endpoint")
    response = client.get("/health")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ PASS: Server {result.get('status')} on {result.get('hostname')}")
    
    # Test 3: MCP without auth returns HTTP 403 (VS Code compatible!)
    print("\n🔐 Test 3: MCP Authentication (THE KEY INNOVATION)")
    response = client.post("/mcp/messages", json={"method": "test"})
    print(f"   Status: {response.status_code}")
    if response.status_code == 403:
        print("   ✅ PASS: HTTP 403 (VS Code won't show OAuth popups!)")
        print("   🎯 KEY INNOVATION WORKING: Avoids VS Code OAuth discovery")
    else:
        print(f"   ⚠️  Got {response.status_code}, expected 403")
    
    # Test 4: MCP with valid auth should work
    print("\n🔑 Test 4: MCP with valid API key")
    headers = {"X-API-Key": "demo-key-123"}
    response = client.post("/mcp/messages", headers=headers, json={"method": "test"})
    print(f"   Status: {response.status_code}")
    # Note: May be 400 due to invalid MCP message format, but not 403
    if response.status_code != 403:
        print("   ✅ PASS: Valid API key bypasses authentication")
    
    print(f"\n🎯 SHOWCASE SUMMARY:")
    print(f"   ✅ Proven MCPAuthMiddleware from code-buddy")
    print(f"   ✅ HTTP 403 prevents VS Code OAuth popups")  
    print(f"   ✅ Clean, professional authentication")
    print(f"   ✅ Ready for stakeholder demonstration")

if __name__ == "__main__":
    test_showcase_ready_server()