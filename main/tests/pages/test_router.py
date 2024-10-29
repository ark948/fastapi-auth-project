from fastapi.testclient import TestClient


from src.pages.router import router


client = TestClient(router)


def test_pages_index():
    response = client.get('/test')
    assert response.status_code == 200