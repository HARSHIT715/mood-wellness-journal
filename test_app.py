import pytest
from app import app, ENTRIES


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    ENTRIES.clear()
    with app.test_client() as test_client:
        yield test_client
    ENTRIES.clear()


def test_health(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {'status': 'ok'}


def test_valid_entry_is_added(client):
    response = client.post('/add', data={
        'name': 'Harshit',
        'entry_date': '2026-09-25',
        'mood': '5',
        'note': 'Productive study session.'
    })
    assert response.status_code == 302
    assert len(ENTRIES) == 1
    assert ENTRIES[0]['mood'] == 5
    assert ENTRIES[0]['emoji'] == '😄'


def test_invalid_mood_is_rejected(client):
    response = client.post('/add', data={
        'name': 'Harshit',
        'entry_date': '2026-09-25',
        'mood': '6',
        'note': 'Invalid mood test.'
    })
    assert response.status_code == 400
    assert len(ENTRIES) == 0


def test_average_mood(client):
    for mood in ('4', '5'):
        client.post('/add', data={
            'name': 'Test User',
            'entry_date': '2026-09-25',
            'mood': mood,
            'note': 'Average test.'
        })
    response = client.get('/api/entries')
    assert response.status_code == 200
    assert response.get_json()['average_mood'] == 4.5


def test_api_returns_entries(client):
    client.post('/add', data={
        'name': 'API User',
        'entry_date': '2026-09-25',
        'mood': '3',
        'note': 'API test.'
    })
    response = client.get('/api/entries')
    assert response.status_code == 200
    assert len(response.get_json()['entries']) == 1
