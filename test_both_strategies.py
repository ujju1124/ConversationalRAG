"""Test both chunking strategies."""
import requests
import time
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("Testing Both Chunking Strategies")
print("=" * 80)

# Wait for server
print("\n⏳ Waiting for server to be ready...")
time.sleep(10)

# Test health check
print("\n1️⃣ Testing health check...")
try:
    r = requests.get(f"{BASE_URL}/")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print("   Make sure server is running!")
    exit(1)

# Test FIXED strategy
print("\n2️⃣ Testing FIXED chunking strategy...")
try:
    with open("sample_document.txt", "rb") as f:
        files = {"file": ("sample_document.txt", f)}
        params = {"strategy": "fixed"}
        r = requests.post(f"{BASE_URL}/ingest", files=files, params=params)
    
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        result = r.json()
        print(f"   ✅ SUCCESS!")
        print(f"   Document ID: {result['document_id']}")
        print(f"   Chunk Count: {result['chunk_count']}")
        print(f"   Strategy: {result['strategy']}")
        fixed_doc_id = result['document_id']
    else:
        print(f"   ❌ FAILED!")
        print(f"   Response: {r.text}")
        fixed_doc_id = None
except Exception as e:
    print(f"   ❌ Error: {e}")
    fixed_doc_id = None

time.sleep(2)

# Test SENTENCE strategy
print("\n3️⃣ Testing SENTENCE chunking strategy...")
try:
    with open("sample_document.txt", "rb") as f:
        files = {"file": ("sample_document.txt", f)}
        params = {"strategy": "sentence"}
        r = requests.post(f"{BASE_URL}/ingest", files=files, params=params)
    
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        result = r.json()
        print(f"   ✅ SUCCESS!")
        print(f"   Document ID: {result['document_id']}")
        print(f"   Chunk Count: {result['chunk_count']}")
        print(f"   Strategy: {result['strategy']}")
        sentence_doc_id = result['document_id']
    else:
        print(f"   ❌ FAILED!")
        print(f"   Response: {r.text}")
        sentence_doc_id = None
except Exception as e:
    print(f"   ❌ Error: {e}")
    sentence_doc_id = None

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"FIXED Strategy:    {'✅ WORKS' if fixed_doc_id else '❌ FAILED'}")
print(f"SENTENCE Strategy: {'✅ WORKS' if sentence_doc_id else '❌ FAILED'}")
print("=" * 80)

if fixed_doc_id and sentence_doc_id:
    print("\n🎉 Both strategies are working correctly!")
else:
    print("\n⚠️ Some strategies failed - check the logs above")
