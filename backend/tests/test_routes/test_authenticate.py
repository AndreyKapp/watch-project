from fastapi.testclient import TestClient


def test_authenticate_user(client: TestClient):
    response = client.post(
        '/token/', 
        data={
            'username': 'test',
            'password': 'test',
        }
    )
    assert response.status_code == 200, 'Get token failed'
