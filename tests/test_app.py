from fastapi.testclient import TestClient
from app.main import app


def test_login_page():
    c = TestClient(app)
    r = c.get('/login')
    assert r.status_code == 200


def test_jwt_auth_fail():
    c = TestClient(app)
    r = c.post('/api/auth/token', params={'username':'bad','password':'bad'})
    assert r.status_code == 401
