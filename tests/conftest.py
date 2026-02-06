"""
Test Configuration
CSIR EOI 8119 - Mining Data Analytics API
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session."""
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Get authentication headers for protected endpoints."""
    # Register a test user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User",
            "role": "admin"
        }
    )
    
    # Login to get token
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "TestPass123"}
    )
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}
