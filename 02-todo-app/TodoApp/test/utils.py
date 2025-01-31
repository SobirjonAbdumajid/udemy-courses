from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from TodoApp.database import Base
from TodoApp.main import app
from TodoApp.models import Todos
import pytest


SQLALCHEMY_DATABASE_URI = 'sqlite:///./testdb.db'
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'string', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn code',
        description="don't give up",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with TestingSessionLocal() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()
        # db.delete(todo)
    # db.rollback()