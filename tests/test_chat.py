"""Tests for conversational RAG API."""
import pytest


def test_chat_endpoint_basic(test_client, mock_groq, mock_pinecone, mock_redis):
    """Test basic chat functionality with mocked dependencies."""
    # First create a document
    from io import BytesIO
    test_content = "Machine learning is a subset of artificial intelligence."
    file_data = BytesIO(test_content.encode('utf-8'))
    
    ingest_response = test_client.post(
        "/ingest?strategy=fixed",
        files={"file": ("ml_doc.txt", file_data, "text/plain")}
    )
    assert ingest_response.status_code == 200
    document_id = ingest_response.json()["document_id"]
    
    # Now chat about it
    chat_response = test_client.post(
        "/chat",
        json={
            "session_id": "test-session-1",
            "user_message": "What is machine learning?",
            "document_id": document_id
        }
    )
    
    assert chat_response.status_code == 200
    data = chat_response.json()
    assert "response" in data
    assert "session_id" in data
    assert data["session_id"] == "test-session-1"
    assert "booking" in data
    
    # Verify mocks were actually used instead of real API calls
    assert mock_pinecone.query.called, "Mock Pinecone query was not called - real API may have been used"
    assert mock_redis.rpush.called, "Mock Redis rpush was not called - real Redis may have been used"


def test_chat_with_invalid_document_id(test_client):
    """Test that chat with non-existent document returns 404."""
    response = test_client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "user_message": "Hello",
            "document_id": "non-existent-id"
        }
    )
    
    assert response.status_code == 404
    assert "Document not found" in response.json()["detail"]


def test_chat_response_schema(test_client):
    """Test that chat response matches expected schema."""
    from io import BytesIO
    file_data = BytesIO(b"Test content for schema validation.")
    
    ingest_response = test_client.post(
        "/ingest?strategy=fixed",
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    document_id = ingest_response.json()["document_id"]
    
    chat_response = test_client.post(
        "/chat",
        json={
            "session_id": "schema-test",
            "user_message": "Test message",
            "document_id": document_id
        }
    )
    
    assert chat_response.status_code == 200
    data = chat_response.json()
    
    # Verify schema
    assert isinstance(data["response"], str)
    assert isinstance(data["session_id"], str)
    assert data["booking"] is None or isinstance(data["booking"], dict)


def test_chat_missing_required_fields(test_client):
    """Test that missing required fields return 422."""
    # Missing user_message
    response = test_client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "document_id": "some-id"
        }
    )
    
    assert response.status_code == 422  # Validation error
