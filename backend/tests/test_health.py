from app.models import User
import pytest
from sqlalchemy.orm import Session
from app.database import test_engine
from fastapi.testclient import TestClient

from app.main import app, get_db


@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    db = Session(
        bind=connection,
        join_transaction_mode="create_savepoint"
    )

    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()
@pytest.fixture
def sample_user(db_session):
    user = User(name="TestUser")
    db_session.add(user)
    db_session.flush()
    return user


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.pop(get_db, None)

def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
def test_users(client, sample_user):
    response = client.get("/users")

    assert response.status_code == 200

    users = response.json()

    assert len(users) == 1
    assert users[0]["name"] == sample_user.name

def test_rollback(db_session):
    user = User(name="RollbackCheck")

    db_session.add(user)
    db_session.flush()

    result = db_session.query(User).filter_by(
        name="RollbackCheck"
    ).first()

    assert result is not None
