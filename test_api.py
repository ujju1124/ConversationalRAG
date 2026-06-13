"""Simple script to test the RAG API end-to-end."""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint."""
    print("\n🔍 Testing health check...")
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

def test_document_ingestion():
    """Test document upload and ingestion."""
    print("\n📄 Testing document ingestion...")
    
    # Upload sample document
    with open("sample_document.txt", "rb") as f:
        files = {"file": ("sample_document.txt", f)}
        params = {"strategy": "sentence"}
        response = requests.post(
            f"{BASE_URL}/ingest",
            files=files,
            params=params
        )
    
    print(f"✅ Status: {response.status_code}")
    result = response.json()
    print(f"Document ID: {result['document_id']}")
    print(f"Filename: {result['filename']}")
    print(f"Chunks: {result['chunk_count']}")
    print(f"Strategy: {result['strategy']}\n")
    
    return result['document_id'] if response.status_code == 200 else None

def test_chat(document_id, session_id="test-session-123"):
    """Test chat with the uploaded document."""
    print("\n💬 Testing chat endpoint...")
    
    # Test 1: General question
    print("\n📝 Question 1: What is machine learning?")
    payload = {
        "session_id": session_id,
        "user_message": "What is machine learning?",
        "document_id": document_id
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    result = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {result['response'][:200]}...")
    print(f"Booking: {result['booking']}\n")
    
    time.sleep(1)  # Rate limiting
    
    # Test 2: Follow-up question (tests chat history)
    print("\n📝 Question 2: What are its types?")
    payload = {
        "session_id": session_id,
        "user_message": "What are its types?",
        "document_id": document_id
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    result = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {result['response'][:200]}...")
    print(f"Booking: {result['booking']}\n")
    
    time.sleep(1)  # Rate limiting
    
    # Test 3: Booking intent
    print("\n📝 Question 3: I'd like to schedule an interview")
    payload = {
        "session_id": session_id,
        "user_message": "I'd like to schedule an interview for Jane Smith at jane@example.com on Monday at 2 PM",
        "document_id": document_id
    }
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    result = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"Response: {result['response'][:200]}...")
    print(f"Booking: {result['booking']}\n")

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 RAG API Test Suite")
    print("=" * 60)
    
    try:
        # Test 1: Health check
        if not test_health_check():
            print("❌ Health check failed. Is the server running?")
            return
        
        # Test 2: Document ingestion
        document_id = test_document_ingestion()
        if not document_id:
            print("❌ Document ingestion failed.")
            return
        
        # Wait for Pinecone indexing
        print("⏳ Waiting 5 seconds for vector indexing...")
        time.sleep(5)
        
        # Test 3: Chat functionality
        test_chat(document_id)
        
        print("=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python run_server.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
