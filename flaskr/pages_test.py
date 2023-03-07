from flaskr import create_app

import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def test_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to the Pokemon Wiki" in resp.data

# TODO(Project 1): Write tests for other routes.

def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Edgar Ochoa Sotelo" in resp.data
    assert b"Mark Toro" in resp.data
    assert b"Javier Garcia" in resp.data

def test_pages(client):
    resp = client.get("/pages")

def test_sign_up(client):
    data={'username': 'username', 'password': 'password'}
    resp = client.post('/signup', data=data)
    assert resp.status_code == 200
    assert b'username' in resp.data
    assert b'Sign Up' in resp.data

def test_sign_in(client):
    data={'username': 'marktoro', 'password': 'mypassword'}
    resp = client.post('login', data=data)
    assert resp.status_code == 200
    assert b'marktoro' in resp.data
    assert b'Log In' in resp.data

def test_logout(client):
    resp = client.post('/logout')
    assert resp.status_code == 302 # Redirection found
    assert 'login' in resp.location