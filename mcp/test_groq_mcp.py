"""
Test TempMail MCP Server with Groq

Usage:
    export GROQ_API_KEY=your_api_key
    source .venv/bin/activate
    python mcp/test_groq_mcp.py

This script tests:
1. Groq API directly
2. MCP tools directly (via langchain-mcp-adapters)
3. Groq + MCP combined (manual prompt engineering)
"""

import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from groq import Groq
from langchain_mcp_adapters.client import MultiServerMCPClient

MCP_CONFIG = {
    "tempmail": {
        "transport": "stdio",
        "command": "uv",
        "args": ["--directory", os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "run", "python", "mcp/server.py"],
    }
}


def get_text(result):
    """Extract text from MCP tool result"""
    if isinstance(result, list):
        for item in result:
            if isinstance(item, dict):
                return item.get('text', json.dumps(item))
    elif isinstance(result, dict):
        return result.get('text', json.dumps(result))
    return str(result)


def test_groq_api():
    """Test Groq API directly"""
    print("\n" + "=" * 60)
    print("1. Testing Groq API")
    print("=" * 60)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not set! Run: export GROQ_API_KEY=your_key")
        return False
    
    try:
        client = Groq(api_key=api_key)
        chat = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Groq API working!'"}],
            max_tokens=20,
        )
        response = chat.choices[0].message.content
        print(f"✅ Groq Response: {response}")
        return True
    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return False


async def test_mcp_direct():
    """Test MCP tools directly"""
    print("\n" + "=" * 60)
    print("2. Testing MCP Tools Directly")
    print("=" * 60)
    
    try:
        client = MultiServerMCPClient(MCP_CONFIG)
        tools = await client.get_tools()
        print(f"✅ Connected to MCP server")
        print(f"✅ Found {len(tools)} tools: {', '.join(t.name for t in tools)}")
        
        results = {}
        
        get_email = next((t for t in tools if t.name == "get_temp_email"), None)
        if get_email:
            print("\n   Testing get_temp_email...")
            result = await get_email.ainvoke({"provider": "tempmailo"})
            text = get_text(result)
            email = json.loads(text)["email"]
            results["email"] = email
            print(f"   ✅ Email: {email}")
        
        extract = next((t for t in tools if t.name == "extract_urls"), None)
        if extract:
            print("\n   Testing extract_urls...")
            result = await extract.ainvoke({"content": "Visit https://example.com and https://google.com"})
            text = get_text(result)
            urls = json.loads(text)
            results["urls"] = urls
            print(f"   ✅ URLs: {urls}")
        
        inbox = next((t for t in tools if t.name == "check_inbox"), None)
        if inbox:
            print("\n   Testing check_inbox...")
            result = await inbox.ainvoke({"email": results.get("email", "test@example.com"), "provider": "tempmailo"})
            print(f"   ✅ Inbox checked successfully")
        
        read_msg = next((t for t in tools if t.name == "read_message"), None)
        if read_msg:
            print("\n   Testing read_message...")
            result = await read_msg.ainvoke({"email": "test@example.com", "message_id": "123", "provider": "tempmailo"})
            print(f"   ✅ Read message checked successfully")
        
        return True
    except Exception as e:
        print(f"❌ MCP Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_groq_mcp_combined():
    """Test Groq + MCP combined"""
    print("\n" + "=" * 60)
    print("3. Testing Groq + MCP Combined")
    print("=" * 60)
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not set!")
        return False
    
    try:
        client = MultiServerMCPClient(MCP_CONFIG)
        tools = await client.get_tools()
        get_email_tool = next((t for t in tools if t.name == "get_temp_email"), None)
        extract_tool = next((t for t in tools if t.name == "extract_urls"), None)
        
        if not get_email_tool or not extract_tool:
            print("❌ Required tools not found")
            return False
        
        groq_client = Groq(api_key=api_key)
        
        print("\n   Step 1: Get temp email via MCP...")
        email_result = await get_email_tool.ainvoke({"provider": "tempmailo"})
        email = json.loads(get_text(email_result))["email"]
        print(f"   ✅ Got email: {email}")
        
        print("\n   Step 2: Use Groq for recommendation...")
        prompt = f"User has temp email: {email}. What should they do next? Reply in 1 sentence."
        chat = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50,
        )
        print(f"   ✅ Recommendation: {chat.choices[0].message.content}")
        
        print("\n   Step 3: Test URL extraction...")
        url_result = await extract_tool.ainvoke({
            "content": "Click https://verify.com/123 to confirm your account"
        })
        urls = json.loads(get_text(url_result))
        print(f"   ✅ Extracted: {urls}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_all_providers():
    """Test all MCP providers"""
    print("\n" + "=" * 60)
    print("4. Testing All MCP Providers")
    print("=" * 60)
    
    try:
        client = MultiServerMCPClient(MCP_CONFIG)
        tools = await client.get_tools()
        get_email_tool = next((t for t in tools if t.name == "get_temp_email"), None)
        
        for provider in ["tempmailo", "mailtm", "tempmailplus"]:
            print(f"\n   Testing {provider}...")
            result = await get_email_tool.ainvoke({"provider": provider})
            data = json.loads(get_text(result))
            email = data.get("email", data)
            print(f"   ✅ {provider}: {email}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def main():
    print("\n" + "🚀" + "=" * 58 + "🚀")
    print("  TempMail MCP Server + Groq API Test")
    print("🚀" + "=" * 58 + "🚀\n")
    
    results = {}
    results["groq_api"] = test_groq_api()
    results["mcp_direct"] = await test_mcp_direct()
    results["mcp_groq"] = await test_groq_mcp_combined()
    results["all_providers"] = await test_all_providers()
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Groq API:        {'✅ PASS' if results.get('groq_api') else '❌ FAIL'}")
    print(f"MCP Direct:      {'✅ PASS' if results.get('mcp_direct') else '❌ FAIL'}")
    print(f"Groq + MCP:      {'✅ PASS' if results.get('mcp_groq') else '❌ FAIL'}")
    print(f"All Providers:   {'✅ PASS' if results.get('all_providers') else '❌ FAIL'}")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    print(f"\n🎉 {passed}/{len(results)} tests passed!")
    
    return all(results.values())


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
