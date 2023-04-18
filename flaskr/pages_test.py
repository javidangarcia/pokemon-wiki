from flaskr import create_app
from flask import render_template, json, request
from unittest.mock import MagicMock, patch
import pytest
import base64

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


@pytest.fixture
def backend():
    return MagicMock()


@pytest.fixture
def hashfunc():
    return MagicMock


@pytest.fixture
def base64func():
    return MagicMock


@pytest.fixture
def fake_file():
    return MagicMock()

@pytest.fixture
def mock_rand():
    return MagicMock()

@patch("flaskr.backend.Backend.get_image",
       return_value=b"This should have been a real image!")
def test_home_page(mock_get_wiki_page, client):

    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Pokemon Wiki" in response.data
    assert b"This should have been a real image!" in response.data


# Tests about page, should return author's names
@patch("flaskr.backend.Backend.get_image",
       return_value=b"This is an image too!")
def test_about_page(mock_get_image, client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Edgar Ochoa Sotelo" in resp.data
    assert b"Mark Toro" in resp.data
    assert b"Javier Garcia" in resp.data
    assert b"This is an image too!" in resp.data

"""
# should return list of pages
def test_pages(client):
    with patch("flaskr.backend.Backend.get_all_page_names",
               return_value=["User Generated Pages"]):
        response = client.get("/pages")
        assert response.status_code == 200
        assert b"User Generated Pages" in response.data
"""

# should return back to upload page
def test_upload_get(client):
    response = client.get("/upload")
    assert response.status_code == 302
    assert "upload" in response.location

"""
# should return page for abra
@patch("flaskr.backend.Backend.get_wiki_page", return_value=b"{'name':'diff'}")
@patch("flask.json.loads",
       return_value={
           'name': 'abra',
           'type': '',
           'region': '',
           'nature': '',
           'level': '',
           'image-name': '',
           'image-type': ''
       })
def test_get_wiki_page(mock_json, mock_get_page, client):
    response = client.get("/pages/abra")
    assert b"abra" in response.data
    mock_json.assert_called_once_with(b"{'name':'diff'}")
"""

# Tests sign up page
def test_sign_up(client):
    data = {'username': 'username', 'password': 'password'}
    resp = client.post('/signup', data=data)
    assert resp.status_code == 200
    assert b'username' in resp.data
    assert b'Sign Up' in resp.data


# Tests sign in page
def test_sign_in(client):
    data = {'username': 'marktoro', 'password': 'mypassword'}
    resp = client.post('login', data=data)
    assert resp.status_code == 200
    assert b'marktoro' in resp.data
    assert b'Log In' in resp.data


# Tests logout redirect
def test_logout(client):
    resp = client.post('/logout')
    assert resp.status_code == 302  # Redirection found
    assert 'login' in resp.location


@patch("flaskr.backend.Backend.upload",
       return_value=b"Uploaded a test pokemon!")
@patch("flaskr.backend.Backend.get_all_page_names",
       return_value=["name1", "name2", "name3"])
def test_upload_post(mock_get_all_pages, mock_upload, app, client):
    with app.test_request_context("",
                                  query_string={
                                      'name': 'abra',
                                      'type': '',
                                      'region': '',
                                      'nature': '',
                                      'level': '',
                                      'image-name': '',
                                      'image-type': ''
                                  }):
        response = client.post("/upload")
        #assert response.status_code == 0
        assert request.args.get("name") == "abra"
        assert mock_upload() == b"Uploaded a test pokemon!"
        assert mock_get_all_pages() == ["name1", "name2", "name3"]
"""

def test_game(client,app):
    with app.test_request_context("",
                                query_string={
                                    'name': 'abra',
                                    'image': 'asdfEFDDSEDFEE',
                                }):
        response = client.get("/game")
        assert request.args.get("name") == "abra"
        assert request.args.get("image") == "asdfEFDDSEDFEE"           


def test_game_post(app, client):
    with app.test_request_context("",
                                  query_string={
                                      'name': 'abra',
                                      'rank': '5',
                                      'user': 'user1',
                                      'nature': '',
                                      'level': '',
                                      'image-name': '',
                                      'image-type': ''
                                  }):
        response = client.post("/game")
        assert request.args.get("name") == "abra"
        assert request.args.get("rank") == "5"
        assert request.args.get("user") == "user1"

"""