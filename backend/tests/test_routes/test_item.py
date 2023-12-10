from fastapi.testclient import TestClient

from ..conftest import access_token


def test_item_create(client: TestClient):
    response = client.post(
        '/item/',
        headers={
            'Authorization': f'Bearer {access_token}'
        },
        data={
            'title': 'test watch',
            'description': 'test watch',
            'price': '60'
        },
        files={'image': ('test_file', b'', 'image/png')}
    )
    assert response.status_code == 201, 'Item object was not created'

def test_item_delete(client: TestClient):
    item_id = 1
    error_msg = 'Item wasn\'t deleted from server'
    response = client.delete(
        f'/item/{item_id}/', 
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    assert response.status_code == 200, error_msg
    response = client.get('/item/')
    assert len(response.json()) == 0, error_msg

def test_item_read(client: TestClient):
    item_id = 1
    error_msg = 'Item wasn\'t received from server'
    response = client.get(f'/item/{item_id}/')
    assert response.status_code == 200, error_msg
    item_data = response.json()
    assert item_data['id'] == 1, error_msg

def test_items_read(client: TestClient):
    error_msg = 'List of items wasn\'t received'
    response = client.get('/item/')
    assert response.status_code == 200, error_msg
    assert len(response.json()) == 1, error_msg
