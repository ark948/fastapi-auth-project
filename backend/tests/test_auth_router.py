from src.apps.auth.models import User
from src.apps.auth.utils import generateOtp

def test_create_user_incomplete(client):
    response = client.post(
        '/auth/create',
        json={'email': 'testuser02@gmail.com'}
    )
    assert response.status_code == 422
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_create_user_invalid_email(session, client):
    response = client.post(
        '/auth/create',
        json={'email': 'testuser', 'password': "123"}
    )
    assert response.status_code == 422

    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data == []


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
    assert data['is_active'] == False

    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data != []


def test_read_users(client):
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_table_is_not_empty(session, client):
    user1 = User(email="testuser01@gmail.com", password="123")
    user1.vcode = generateOtp()
    session.add(user1)
    session.commit()
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data[0]['email'] == 'testuser01@gmail.com'


def test_user_table_more_than_one(session, client):
    vcode1 = generateOtp()
    vcode2 = generateOtp()
    user1 = User(email="testuser01@gmail.com", password="123", vcode=vcode1)
    user2 = User(email='testuser02@gmail.com', password='123', vcode=vcode2)
    session.add(user1)
    session.add(user2)
    session.commit()
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['email'] == 'testuser01@gmail.com'
    assert data[1]['email'] == 'testuser02@gmail.com'
    assert data[0]['vcode'] == vcode1
    assert data[1]['vcode'] == vcode2


def test_activate_user(session, client):
    vcode = generateOtp()
    user = User(email='test1@test.com', password='123', vcode=vcode)
    session.add(user)
    session.commit()
    resposne = client.get('/auth/get-all-users')
    assert resposne.status_code == 200
    data = resposne.json()
    assert len(data) == 1
    assert data[0]['id'] == 1
    assert data[0]['is_active'] == False
    response = client.post('/auth/verify-user/1', json={"vcode": vcode})
    assert response.status_code == 200
    response = client.get('/auth/1')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert data['email'] == 'test1@test.com'
    assert data['is_active'] == True


def test_get_user(session, client):
    vcode = generateOtp()
    user = User(email='test1@test.com', password='123', vcode=vcode)
    session.add(user)
    session.commit()

    response = client.get('/auth/1')
    assert response.status_code == 200

    data = response.json()
    assert data['id'] == 1
    assert data['email'] == 'test1@test.com'


def test_update_user(session, client):
    vcode = generateOtp()
    user = User(email='test1@test.com', password='123', vcode=vcode)
    session.add(user)
    session.commit()

    response = client.patch('/auth/1', json={'first_name': "Neal"})
    assert response.status_code == 202
    data = response.json()
    assert data['message'] == 'User with 1 updated.'

    response = client.get('/auth/1')
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'test1@test.com'
    assert data['first_name'] == 'Neal'


def test_delete_user(session, client):
    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert data == []

    user = User(email='test1@test.com', password='123', vcode=generateOtp())
    session.add(user)
    session.commit()

    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    response = client.delete('/auth/1')
    assert response.status_code == 200
    data = response.json()
    assert data['ok'] == True

    response = client.get('/auth/get-all-users')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0