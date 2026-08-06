"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import Mock, MagicMock
from fastapi.testclient import TestClient


@pytest.fixture
def mock_embedding_model(monkeypatch):
    """Mock the embedding model to avoid loading the real model."""
    mock_model = Mock()
    mock_model.encode.return_value = [[0.1] * 384]  # 384-dim mock embedding
    
    def mock_get_model():
        return mock_model
    
    monkeypatch.setattr("app.core.embedding_model.get_embedding_model", mock_get_model)
    monkeypatch.setattr("app.core.embedding_model.generate_embeddings", 
                        lambda texts: [[0.1] * 384 for _ in texts])
    return mock_model


@pytest.fixture
def mock_pinecone(monkeypatch):
    """Mock Pinecone client to avoid real API calls."""
    mock_index = Mock()
    mock_index.upsert.return_value = {"upserted_count": 1}
    mock_index.query.return_value = {
        "matches": [
            {
                "id": "test_1",
                "score": 0.9,
                "metadata": {
                    "text": "Machine learning is a subset of AI.",
                    "document_id": "test-doc-id",
                    "chunk_index": 0
                }
            }
        ]
    }
    
    # Mock query response to have .matches attribute
    mock_query_response = MagicMock()
    mock_query_response.matches = [
        MagicMock(
            metadata={
                "text": "Machine learning is a subset of AI.",
                "document_id": "test-doc-id"
            }
        )
    ]
    mock_index.query.return_value = mock_query_response
    
    monkeypatch.setattr("app.core.pinecone_client.get_pinecone_index", lambda: mock_index)
    return mock_index


@pytest.fixture
def mock_groq(monkeypatch):
    """Mock Groq API client to avoid real API calls."""
    mock_client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="This is a test response."))]
    mock_response.usage = Mock(
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15
    )
    mock_client.chat.completions.create.return_value = mock_response
    
    monkeypatch.setattr("app.services.llm_service.groq_client", mock_client)
    return mock_client


@pytest.fixture
def mock_redis(monkeypatch):
    """Mock Redis client to avoid real connection."""
    mock_client = Mock()
    mock_client.get.return_value = None
    mock_client.setex.return_value = True
    mock_client.lrange.return_value = []
    mock_client.rpush.return_value = 1
    mock_client.delete.return_value = 1
    
    monkeypatch.setattr("app.core.redis_client.get_redis_client", lambda: mock_client)
    return mock_client


@pytest.fixture
def test_client(mock_embedding_model, mock_pinecone, mock_groq, mock_redis):
    """Create a test client with all external dependencies mocked."""
    from app.main import app
    return TestClient(app)
