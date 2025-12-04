import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.core.security import hash_password
from app import models
from fastAPI.run import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

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
    def overrride_get_db():
        try:
            yield db_session
        finally:
            db_session.close
    app.dependency_overrides[get_db] = overrride_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(db_session):
    password = "password123"
    hashed_password = hash_password(password)
    
    user = models.UserDB(
        username="testuser",
        email="test@example.com",
        password=hashed_password # hash password 
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user 
