"""
Backend API Test Suite
Uses pytest to test all API endpoints and functionality.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

# Mock data
TEST_USER = {
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
}

TEST_ITEM = {
    "id": "1234-5678",
    "user_id": "user-123",
    "image_url": "http://example.com/image.jpg",
    "category": "shirt",
    "color": "blue",
    "brand": "TestBrand",
    "notes": "A test item"
}

@pytest.fixture
def mock_supabase():
    with patch("main.supabase") as mock_supabase_client:
        # Mock auth
        mock_auth = MagicMock()
        mock_auth.sign_up.return_value.user.id = "user-123"
        mock_auth.sign_in_with_password.return_value.user.id = "user-123"
        mock_supabase_client.auth = mock_auth
        
        # Mock table operations
        mock_table = MagicMock()
        mock_table.select.return_value.eq.return_value.execute.return_value.data = [TEST_ITEM]
        mock_table.insert.return_value.execute.return_value.data = [TEST_ITEM]
        mock_table.update.return_value.eq.return_value.execute.return_value.data = [TEST_ITEM]
        mock_table.delete.return_value.eq.return_value.execute.return_value.data = []
        mock_supabase_client.table.return_value = mock_table
        
        # Mock storage
        mock_storage = MagicMock()
        mock_storage.from_.return_value.upload.return_value = None
        mock_storage.from_.return_value.get_public_url.return_value = "http://example.com/image.jpg"
        mock_supabase_client.storage = mock_storage
        
        yield mock_supabase_client

@pytest.fixture
def mock_openai():
    with patch("ai_recommendations.client") as mock_openai_client:
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = '{"outfits": [{"name": "Test Outfit"}]}'
        mock_openai_client.chat.completions.create.return_value = mock_completion
        yield mock_openai_client

@pytest.fixture
def auth_headers():
    # Mock token generation
    with patch("main.create_access_token") as mock_create_token:
        mock_create_token.return_value = "test-token"
        response = client.post("/api/auth/login", json=TEST_USER)
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


# Test Auth Endpoints
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_signup(mock_supabase):
    response = client.post("/api/auth/signup", json=TEST_USER)
    assert response.status_code == 201
    assert "access_token" in response.json()

def test_login(mock_supabase):
    response = client.post("/api/auth/login", json=TEST_USER)
    assert response.status_code == 200
    assert "access_token" in response.json()


# Test Item Endpoints
def test_get_items(mock_supabase, auth_headers):
    response = client.get("/api/items", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1
    assert response.json()["items"][0]["category"] == "shirt"

def test_upload_item(mock_supabase, auth_headers):
    with open("test_image.jpg", "wb") as f:
        f.write(b"test image data")
    
    with open("test_image.jpg", "rb") as f:
        response = client.post(
            "/api/items/upload",
            files={"file": ("test_image.jpg", f, "image/jpeg")},
            data={"category": "test"},
            headers=auth_headers
        )
    
    os.remove("test_image.jpg")
    assert response.status_code == 200
    assert response.json()["message"] == "Clothing item uploaded successfully"

def test_delete_item(mock_supabase, auth_headers):
    response = client.delete(f"/api/items/{TEST_ITEM['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"


# Test AI Endpoints
def test_get_outfit_recommendations(mock_supabase, mock_openai, auth_headers):
    response = client.post("/api/recommendations/outfits", headers=auth_headers)
    assert response.status_code == 200
    assert "recommendations" in response.json()

def test_analyze_closet(mock_supabase, mock_openai, auth_headers):
    response = client.get("/api/recommendations/closet-analysis", headers=auth_headers)
    assert response.status_code == 200
    assert "analysis" in response.json()


# Test Advanced Feature Endpoints
def test_toggle_favorite(mock_supabase, auth_headers):
    response = client.post(f"/api/items/{TEST_ITEM['id']}/favorite", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["is_favorite"] == True

def test_search_items(mock_supabase, auth_headers):
    response = client.get("/api/items/search?query=test", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) > 0


# Test Social Feature Endpoints
def test_share_outfit(mock_supabase, auth_headers):
    response = client.post(
        "/api/outfits/share",
        json={"outfit_name": "Test Share", "item_ids": [TEST_ITEM["id"]]},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "share_token" in response.json()

def test_plan_outfit(mock_supabase, auth_headers):
    response = client.post(
        "/api/outfits/plan",
        json={"outfit_name": "Test Plan", "item_ids": [TEST_ITEM["id"]], "planned_date": "2025-12-25"},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "plan" in response.json()
