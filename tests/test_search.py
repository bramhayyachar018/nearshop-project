import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sqlite3

from app.main import app
from app.database import Base, get_db
from app.models import Product, Store, Inventory, Retailer

# Use an in-memory SQLite database for testing
# Note: SQLite doesn't have pgvector natively in test mode, so we skip semantic tests
# but we can test text based /search endpoint.

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    from app.models import Product
    from sqlalchemy.dialects.sqlite import BLOB

    # Overwrite the Vector column type specifically for testing with SQLite
    Product.__table__.columns['embedding'].type = BLOB()

    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_search_products_text_match():
    # Setup Data
    db = TestingSessionLocal()

    retailer = Retailer(name="Test Retailer", email="test3@example.com")
    db.add(retailer)
    db.commit()

    store = Store(name="Test Store", address="123 Main St", latitude=10.0, longitude=20.0, retailer_id=retailer.id)
    db.add(store)
    db.commit()

    product1 = Product(name="Wireless Mouse", category="Electronics", price=25.0)
    product2 = Product(name="Mechanical Keyboard", category="Electronics", price=80.0)
    db.add_all([product1, product2])
    db.commit()

    inventory1 = Inventory(store_id=store.id, product_id=product1.id, quantity=10)
    inventory2 = Inventory(store_id=store.id, product_id=product2.id, quantity=0) # out of stock
    db.add_all([inventory1, inventory2])
    db.commit()
    db.close()

    # Search query
    response = client.get("/search/?query=mouse")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    items = data["data"]["items"]
    assert len(items) == 1
    assert items[0]["product"]["name"] == "Wireless Mouse"
    assert items[0]["quantity"] == 10

def test_search_products_location():
    # Setup Data
    db = TestingSessionLocal()

    retailer = Retailer(name="Test Retailer 2", email="test4@example.com")
    db.add(retailer)
    db.commit()

    # Store close to user (0.0, 0.0)
    store1 = Store(name="Store Near", address="123 Near St", latitude=1.0, longitude=1.0, retailer_id=retailer.id)
    # Store far from user
    store2 = Store(name="Store Far", address="456 Far St", latitude=50.0, longitude=50.0, retailer_id=retailer.id)
    db.add_all([store1, store2])
    db.commit()

    product = Product(name="Water Bottle", category="Home", price=15.0)
    db.add(product)
    db.commit()

    inv1 = Inventory(store_id=store1.id, product_id=product.id, quantity=5)
    inv2 = Inventory(store_id=store2.id, product_id=product.id, quantity=5)
    db.add_all([inv1, inv2])
    db.commit()

    # Capture IDs before closing the DB session to prevent DetachedInstanceError
    s1_id = store1.id
    s2_id = store2.id

    db.close()

    # Search ordered by location (0,0)
    response = client.get("/search/?lat=0.0&lng=0.0")
    assert response.status_code == 200
    data = response.json()

    items = data["data"]["items"]
    assert len(items) == 2
    # The nearest store should be first
    assert items[0]["store_id"] == s1_id
    assert items[1]["store_id"] == s2_id
