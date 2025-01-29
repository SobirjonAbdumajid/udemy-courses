from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import Todos


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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            'id': 1,
            "title": "Learn code",
            "description": "don't give up",
            "priority": 5,
            "complete": False,
            "owner_id": 1
        }
    ]


def test_read_one_authenticated(test_todo):
    response = client.get('/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        "title": "Learn code",
        "description": "don't give up",
        "priority": 5,
        "complete": False,
        "owner_id": 1
    }


def test_read_todo_authenticated_not_found():
    response = client.get('/todo/999')  # Test a non-existent ID
    assert response.json()['status_code'] == 404
    assert response.json() == {'detail': 'Todo not found', 'headers': None, 'status_code': 404}


def test_create_todo(test_todo):
    request_data={
        'title': 'New Todo!',
        'description':'New todo description',
        'priority': 5,
        'complete': False,
    }

    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')