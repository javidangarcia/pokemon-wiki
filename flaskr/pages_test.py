from flaskr import create_app
from flask import render_template, json
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
def mockend():
    return MagicMock()
"""
# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
@patch("flaskr.backend.Backend.get_image",return_value="not an actual image")
def test_home_page(client,mockend):
    mockend.get_image.return_value = "image file"
    response = client.get("/", mockend)
    print(response.data)
    assert b"image file" in response.data
    #assert response.status_code == 200
    #assert b"Welcome to the Pokemon Wiki" in response.data
    #assert b"Browse, upload, have fun." in response.data
"""
# Tests about page, should return author's names
def test_about_page(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Edgar Ochoa Sotelo" in resp.data
    assert b"Mark Toro" in resp.data
    assert b"Javier Garcia" in resp.data
"""
# should return list of pages
def test_pages(client):
    with patch("flaskr.backend.Backend.get_all_page_names",return_value=["User Generated Pages"]):
        response = client.get("/pages")
        assert response.status_code == 200
        assert b"User Generated Pages" in response.data




# should return back to upload page
def test_upload_get(client):
    response = client.get("/upload")
    assert response.status_code == 302
    assert "upload" in response.location

# returns bad request error code, client must have app running in order to function. 
# but app cannot run while testing.
#@patch("flaskr.backend.Backend.upload",return_value="uploaded")
def test_upload_post(client):
    form_dict = '{"name":"abra","hit_points":"999","image":"NONE","attack":"999","defense":"999","speed":"999","special_attack":"999","special_defense":"999","type":"999"}'
    form = json.dumps(form_dict)
    response = client.post("/upload", data=form, headers={'Content-Type':'application/json'})
    assert response.status_code == 400
  
# should return page for abra
@patch("flaskr.backend.Backend.get_wiki_page", return_value="{"+"abra"+"}")
#@patch("json.loads",return_value="abra")
def test_get_wiki_page(client):
    response = client.get("/pages/abra")
    #assert response.status_code == 200
    #assert b"abra" in response.data

# Tests sign up page
def test_sign_up(client):
    data={'username': 'username', 'password': 'password'}
    resp = client.post('/signup', data=data)
    assert resp.status_code == 200
    assert b'username' in resp.data
    assert b'Sign Up' in resp.data

# Tests sign in page
def test_sign_in(client):
    data={'username': 'marktoro', 'password': 'mypassword'}
    resp = client.post('login', data=data)
    assert resp.status_code == 200
    assert b'marktoro' in resp.data
    assert b'Log In' in resp.data

# Tests logout redirect
def test_logout(client):
    resp = client.post('/logout')
    assert resp.status_code == 302 # Redirection found
    assert 'login' in resp.location

"""