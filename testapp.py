from app import app

def test_home_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200

def test_health_api():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200