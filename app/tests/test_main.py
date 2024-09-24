from urllib import response

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Product

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def test_create_product(client):
    response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 1000, "description": "A powerful laptop", "stock_quantity": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 1000
    assert data["description"] == "A powerful laptop"
    assert data["stock_quantity"] == 10


def test_get_product(client):
    client.post(
        "/products/",
        json={"name": "Laptop", "price": 1000, "description": "A powerful laptop", "stock_quantity": 10},
    )

    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Laptop"


def test_create_product_duplicate_name(client):
    client.post(
        "/products/",
        json={"name": "Laptop", "price": 1000, "description": "A powerful laptop", "stock_quantity": 10},
    )

    response = client.post(
        "/products/",
        json={"name": "Laptop", "price": 1200, "description": "Another laptop", "stock_quantity": 5},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Product with this name already exists"


def test_create_order(client, test_create_product):
    response = client.post(
        "/orders/",
        json={
            "status": "в процессе",
            "order_items": [
                {
                    "product_id": 1,
                    "quantity": 10
                }
            ]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "в процессе"


def test_update_order_status(client, test_create_product):
    response = client.post(
        "/orders/",
        json={
            "status": "в процессе",
            "order_items": [
                {"product_id": 1, "quantity": 2}
            ]
        }
    )
    assert response.status_code == 200

    response = client.patch("/orders/1/status", json={"status": "доставлен"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "доставлен"
