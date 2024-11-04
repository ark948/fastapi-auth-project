


def test_main_app(client):
    response = client.get('/test')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Hello World test"


def test_auth_app_test_route(client):
    response = client.get('/auth/test-route')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Testing auth app..."


def test_pages_app_test_route(client):
    response = client.get('/test-route')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Testing pages app..."
