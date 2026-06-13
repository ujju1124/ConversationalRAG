"""Test booking extraction with improved JSON mode."""
import requests
import json

# Test booking detection
print("=" * 60)
print("Testing Booking Detection with JSON Mode")
print("=" * 60)

# Upload document first (if needed)
print("\n1. Uploading document...")
with open('sample_document.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/ingest?strategy=sentence',
        files={'file': f}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        document_id = data['document_id']
        print(f"Document ID: {document_id}")
    else:
        print(f"Error: {response.text}")
        exit(1)

# Test 1: Booking with all fields
print("\n" + "=" * 60)
print("Test 1: Booking with ALL fields")
print("=" * 60)
payload = {
    "session_id": "test-booking-1",
    "user_message": "I want to schedule an interview for Alice Smith at alice@example.com on Friday at 3 PM",
    "document_id": document_id
}
print(f"\nRequest: {json.dumps(payload, indent=2)}")

response = requests.post(
    'http://localhost:8000/chat',
    json=payload
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"\nResponse:")
    print(json.dumps(data, indent=2))
    
    if data.get('booking'):
        print("\n✅ Booking detected and extracted!")
        print(f"   Name: {data['booking']['name']}")
        print(f"   Email: {data['booking']['email']}")
        print(f"   Date: {data['booking']['date']}")
        print(f"   Time: {data['booking']['time']}")
    else:
        print("\n❌ No booking detected (this is wrong!)")
else:
    print(f"Error: {response.text}")

# Test 2: Booking with partial fields
print("\n" + "=" * 60)
print("Test 2: Booking with PARTIAL fields (no email)")
print("=" * 60)
payload = {
    "session_id": "test-booking-2",
    "user_message": "Can you book an interview for Bob Johnson on Monday at 10 AM?",
    "document_id": document_id
}
print(f"\nRequest: {json.dumps(payload, indent=2)}")

response = requests.post(
    'http://localhost:8000/chat',
    json=payload
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"\nResponse:")
    print(json.dumps(data, indent=2))
    
    if data.get('booking'):
        print("\n✅ Booking detected!")
        print(f"   Name: {data['booking']['name']}")
        print(f"   Email: {data['booking']['email']}")
        print(f"   Date: {data['booking']['date']}")
        print(f"   Time: {data['booking']['time']}")
    else:
        print("\n❌ No booking detected")
else:
    print(f"Error: {response.text}")

# Test 3: No booking (regular question)
print("\n" + "=" * 60)
print("Test 3: Regular question (NO booking)")
print("=" * 60)
payload = {
    "session_id": "test-booking-3",
    "user_message": "What is machine learning?",
    "document_id": document_id
}
print(f"\nRequest: {json.dumps(payload, indent=2)}")

response = requests.post(
    'http://localhost:8000/chat',
    json=payload
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"\nResponse (truncated):")
    print(f"   Answer: {data['response'][:100]}...")
    
    if data.get('booking'):
        print("\n❌ Booking detected (this is wrong!)")
    else:
        print("\n✅ No booking detected (correct!)")
else:
    print(f"Error: {response.text}")

print("\n" + "=" * 60)
print("Testing Complete!")
print("=" * 60)
