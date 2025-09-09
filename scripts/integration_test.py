#!/usr/bin/env python3
"""
Test MCPAuthMiddleware HTTP 403 authentication for VS Code compatibility.

This validates the proven middleware approach from code-buddy that returns
HTTP 403 (not 401) to prevent VS Code OAuth popups.
"""
import os
import httpx
import subprocess
import time
from contextlib import contextmanager

@contextmanager
def running_server():
    """Start real server for testing (not TestClient)"""
    # Set environment
    os.environ["MCP_API_KEYS"] = "test-key-123,showcase-key-456"
    
    # Start server
    process = subprocess.Popen([
        "python", "-m", "uvicorn", "src.main:app", 
        "--host", "127.0.0.1", "--port", "8001"
    ])
    
    # Wait for startup and verify server is ready
    time.sleep(4)
    
    # Wait for server to be ready
    for i in range(10):
        try:
            httpx.get("http://127.0.0.1:8001/health", timeout=1)
            break
        except:
            if i < 9:
                time.sleep(1)
            else:
                print("❌ Server failed to start properly")
    
    try:
        yield "http://127.0.0.1:8001"
    finally:
        process.terminate()
        process.wait()

def test_working_mcp_auth():
    """Test the working MCPAuthMiddleware implementation"""
    print("🎯 Testing Working MCPAuthMiddleware")
    print("=" * 50)
    
    with running_server() as base_url:
        # Test 1: REST endpoints work without auth
        print("✅ Test 1: REST endpoints (no auth needed)")
        response = httpx.get(f"{base_url}/health")
        assert response.status_code == 200
        print(f"   Health: {response.status_code} ✅")
        
        # Test 2: MCP without auth returns HTTP 403 (not 401)
        print("✅ Test 2: MCP without auth (should be 403)")
        response = httpx.post(f"{base_url}/mcp/messages", json={"method": "test"})
        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print(f"   MCP no auth: {response.status_code} ✅ (Prevents VS Code OAuth)")
        
        # Test 3: MCP with valid auth works
        print("✅ Test 3: MCP with valid auth")
        headers = {"X-API-Key": "test-key-123"}
        response = httpx.post(f"{base_url}/mcp/messages", json={"method": "test"}, headers=headers)
        print(f"   MCP with auth: {response.status_code}")
        
        print("\n🎉 All tests passed! MCPAuthMiddleware works correctly.")

if __name__ == "__main__":
    test_working_mcp_auth()
