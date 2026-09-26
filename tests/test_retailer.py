import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import Retailer

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    # SQLite doesn't natively support pgvector Vector types
    # This mock prevents the create_all from crashing or creating bad tables for testing
    from app.models import Product
    from sqlalchemy.dialects.sqlite import BLOB

    # Overwrite the Vector column type specifically for testing with SQLite
    Product.__table__.columns['embedding'].type = BLOB()

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_create_retailer():
    response = client.post(
        "/retailers/",
        json={"name": "Test Retailer", "email": "test@example.com", "phone": "1234567890"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"
    assert "id" in data["data"]

def test_get_retailer():
    # First create one
    post_response = client.post(
        "/retailers/",
        json={"name": "Test Retailer 2", "email": "test2@example.com"}
    )
    retailer_id = post_response.json()["data"]["id"]

    # Then get it
    get_response = client.get(f"/retailers/{retailer_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Test Retailer 2"
