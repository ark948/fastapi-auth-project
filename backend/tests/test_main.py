


def test_main_app(client):
    print("--> Test running (1)...")

    response = client.get('/test')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Hello World test"


def test_auth_app_test_route(client):
    print("--> Test running (2)...")

    response = client.get('/auth/test-route')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Testing auth app..."