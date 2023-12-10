from typing import Any
from typing import Generator
 
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.authorization.utils import get_password_hash, create_access_token
from sql.models import User, Item

from commands import push_user_to_db
 
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
#this is to include backend dir in sys.path so that we can import from db,main.py
 
from sql import Base
from dependencies import get_db
from api.base import base_router
 
 
def start_application():
    app = FastAPI()
    app.include_router(base_router)
    return app
 
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
 
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    Base.metadata.create_all(engine)  # Create the tables.
    _app = start_application()
    yield _app
    Base.metadata.drop_all(engine)
 
 
@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    hashed_password = get_password_hash('test')
    session.add(User(username='test', hashed_password=hashed_password))
    item = Item(
        id=1,
        title='test watch',
        description='test_watch',
        price=600,
        image_name='test_watch.png'
    )
    session.add(item)
    session.commit()
    push_user_to_db('test', 'test')
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()
 
 
@pytest.fixture(scope="function")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
 
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass
 
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


access_token=create_access_token(data={"sub": 'test'})
