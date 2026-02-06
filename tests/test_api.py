"""
API Tests
CSIR EOI 8119 - Mining Data Analytics API
"""

import pytest
from datetime import date, datetime


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test root endpoint."""
    
    def test_root(self, client):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data


class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    def test_register_user(self, client):
        """Test user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "SecurePass123",
                "first_name": "New",
                "last_name": "User",
                "role": "operator"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
    
    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email fails."""
        user_data = {
            "email": "duplicate@example.com",
            "password": "SecurePass123",
            "first_name": "First",
            "last_name": "User",
            "role": "operator"
        }
        
        # First registration should succeed
        response1 = client.post("/api/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration should fail
        response2 = client.post("/api/auth/register", json=user_data)
        assert response2.status_code == 400
    
    def test_login(self, client):
        """Test user login."""
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "email": "login@example.com",
                "password": "SecurePass123",
                "first_name": "Login",
                "last_name": "User",
                "role": "operator"
            }
        )
        
        # Then login
        response = client.post(
            "/api/auth/login",
            data={"username": "login@example.com", "password": "SecurePass123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials fails."""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent@example.com", "password": "WrongPass"}
        )
        assert response.status_code == 401
    
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user info."""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "id" in data


class TestEquipmentEndpoints:
    """Test equipment management endpoints."""
    
    def test_create_equipment(self, client, auth_headers):
        """Test creating new equipment."""
        response = client.post(
            "/api/equipment/",
            headers=auth_headers,
            json={
                "equipment_code": "EXC-001",
                "name": "Excavator Model X",
                "equipment_type": "excavator",
                "manufacturer": "CAT",
                "model": "390F",
                "year_manufactured": 2023,
                "capacity_tonnes": 50.0
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["equipment_code"] == "EXC-001"
        assert data["name"] == "Excavator Model X"
    
    def test_get_equipment_list(self, client, auth_headers):
        """Test getting equipment list."""
        # Create some equipment first
        client.post(
            "/api/equipment/",
            headers=auth_headers,
            json={
                "equipment_code": "TRK-001",
                "name": "Haul Truck 1",
                "equipment_type": "truck"
            }
        )
        
        response = client.get("/api/equipment/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
    
    def test_duplicate_equipment_code(self, client, auth_headers):
        """Test creating equipment with duplicate code fails."""
        equipment_data = {
            "equipment_code": "DUP-001",
            "name": "Test Equipment",
            "equipment_type": "drill"
        }
        
        # First creation should succeed
        response1 = client.post("/api/equipment/", headers=auth_headers, json=equipment_data)
        assert response1.status_code == 201
        
        # Second creation should fail
        response2 = client.post("/api/equipment/", headers=auth_headers, json=equipment_data)
        assert response2.status_code == 400


class TestProtectedEndpoints:
    """Test that endpoints require authentication."""
    
    def test_equipment_requires_auth(self, client):
        """Test that equipment endpoints require authentication."""
        response = client.get("/api/equipment/")
        assert response.status_code == 401
    
    def test_shifts_requires_auth(self, client):
        """Test that shifts endpoints require authentication."""
        response = client.get("/api/shifts/")
        assert response.status_code == 401
    
    def test_production_requires_auth(self, client):
        """Test that production endpoints require authentication."""
        response = client.get("/api/production/")
        assert response.status_code == 401
