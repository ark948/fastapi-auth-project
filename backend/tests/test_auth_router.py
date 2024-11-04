
def test_auth_app_test_route(client):
    response = client.get('/auth/test-route')
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "Testing auth app..."


def test_create_user_incomplete(client):
    response = client.post(
        '/auth/create',
        json={'email': 'testuser02@gmail.com'}
    )
    assert response.status_code == 422


def test_create_user(client):
    response = client.post(
        '/auth/create',
        json={"email": 'testuser01@gmail.com', 'password': "123"}
    )
    data = response.json()
    assert response.status_code == 201
    assert data['email'] == 'testuser01@gmail.com'
    assert data['first_name'] == None
    assert data['last_name'] == None
    assert data['password'] != '123'
    assert data['is_active'] == False


def test_read_users(session, client):
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['email'] == 'testuser01@gmail.com'