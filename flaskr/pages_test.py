from flaskr import create_app
from flask import render_template
from unittest.mock import MagicMock
import pytest

# See https://flask.palletsprojects.com/en/2.2.x/testing/ 
# for more info on testing
class mock_backend():
    def __init__(self):
        self.backend = MagicMock()
        #self.backend.get_all_page_names.return_value(["pages/abra","pages/mudkip","pages/bob"])
    #backend.get_all_page_names.return_value(["pages/abra","pages/mudkip","pages/bob"])
    def get_all_page_names(self):
        return ["pages/abra","pages/mudkip","pages/bob"]
    
    def get(self,x):
        if x == "/pages":
            return self.backend.get_all_page_names()


    """
       @app.route("/pages")
        def pages(pages=None):
        backend = Backend()
        pages = backend.get_all_page_names()
        return render_template('pages.html', pages=pages)
    """
    
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
def backend_mock():
    return mock_backend()

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

# work in progress
def test_pages(client,backend_mock):
    #backend = mock_backend()
    pages = backend_mock.get_all_page_names()
    print(pages)
    whole_page = render_template('pages.html', pages=pages)
    print("whole page:",whole_page)
    #client.pages.return_value("pages/bob")
    #resp = client.get("/pages")
    #response = backend_mock.get("/pages")
    assert "pages/abra" in whole_page
   # assert resp.status_code == 200
   # assert b"pages/squirtle" in resp.data
   # assert b"pages/mudkip" in resp.data

