"""Tests for document ingestion API."""
import pytest
from io import BytesIO


def test_ingest_txt_file_fixed_strategy(test_client):
    """Test ingesting a TXT file with fixed chunking strategy."""
    # Create a simple test file
    test_content = "This is a test document. " * 50
    file_data = BytesIO(test_content.encode('utf-8'))
    
    response = test_client.post(
        "/ingest?strategy=fixed",
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["filename"] == "test.txt"
    assert data["strategy"] == "fixed"
    assert data["chunk_count"] > 0


def test_ingest_txt_file_sentence_strategy(test_client):
    """Test ingesting a TXT file with sentence chunking strategy."""
    test_content = "This is sentence one. This is sentence two. This is sentence three."
    file_data = BytesIO(test_content.encode('utf-8'))
    
    response = test_client.post(
        "/ingest?strategy=sentence",
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "document_id" in data
    assert data["filename"] == "test.txt"
    assert data["strategy"] == "sentence"
    assert data["chunk_count"] >= 3  # At least 3 sentences


def test_ingest_invalid_strategy(test_client):
    """Test that invalid strategy is caught and returns error."""
    test_content = "Test content"
    file_data = BytesIO(test_content.encode('utf-8'))
    
    response = test_client.post(
        "/ingest?strategy=invalid",
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    
    # Should return error (either 400 from validation or 500 from service)
    assert response.status_code in [400, 500]
    assert "detail" in response.json()


def test_ingest_unsupported_file_type(test_client):
    """Test that unsupported file types return error."""
    file_data = BytesIO(b"fake docx content")
    
    response = test_client.post(
        "/ingest?strategy=fixed",
        files={"file": ("test.docx", file_data, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    
    # Should return error
    assert response.status_code in [400, 500]
    assert "detail" in response.json()


def test_ingest_missing_strategy_parameter(test_client):
    """Test that missing strategy parameter returns 422."""
    test_content = "Test content"
    file_data = BytesIO(test_content.encode('utf-8'))
    
    response = test_client.post(
        "/ingest",  # No strategy parameter
        files={"file": ("test.txt", file_data, "text/plain")}
    )
    
    assert response.status_code == 422  # Validation error
