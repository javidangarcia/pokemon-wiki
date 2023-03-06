from flaskr.backend import Backend
import pytest
from unittest.mock import MagicMock

def mock_storage_client():
    buckets = { 'wiki-content-techx' : ['pages/', 'pages/charmander', 'pages/squirtle', 'pages/bulbasaur'], 
                'users-passwords-techx' : ['javier', 'mark', 'edgar'] 
                }

    blobs = { 'pages/' : None, 
              'pages/charmander' : ['Charmander', 'Fire', 'Kanto'],
              'pages/squirtle' : ['Squirtle', 'Water', 'Kanto'],
              'pages/bulbasaur' : ['Bulbasaur', 'Fire', 'Kanto'],
              'javier' : "pokemon123"
            }

    class MockStorageClient():
        def __init__(self):
            self.buckets = buckets

        def get_bucket(self, bucket_name):
            if bucket_name in self.buckets:
                return MockBucket(bucket_name)
            else:
                return None

    class MockBucket():
        def __init__(self, bucket_name):
            self.name = bucket_name
            self.blobs = buckets[self.name]

        def get_blob(self, blob_name):
            if blob_name in self.blobs:
                return MockBlob(blob_name)
            else:
                return None
        
        def list_blobs(self, prefix):
            blobs = []
            for blob in buckets[self.name]:
                blobs.append(MockBlob(blob))
            return blobs

        def blob(self, blob_name):
            return MockBlob(blob_name)


    class MockBlob():
        def __init__(self, blob_name):
            self.name = blob_name
            self.content = None

        def open(self, mode):
            return self

        def read(self):
            return blobs[self.name]

        def write(self, text):
            self.content = text

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass
    
    return MockStorageClient()

class MockHashFunction:
    def __init__(self):
        pass    
    
    def blake2b(self, salt):
        return self
    
    def hexdigest(self):
        return "pokemon123"


@pytest.fixture
def mock_storage():
    return mock_storage_client()

@pytest.fixture
def mock_hashfunc():
    return MockHashFunction()    


def test_get_wiki_page():
    client = MagicMock()
    bucket = MagicMock()
    blob = MagicMock()
    f = MagicMock()
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.open.return_value.__enter__.return_value = f
    f.read.return_value = ['Charmander', 'Fire', 'Kanto']
    backend = Backend(client)
    assert backend.get_wiki_page('charmander') == ['Charmander', 'Fire', 'Kanto']


def test_get_all_page_names():
    client = MagicMock()
    bucket = MagicMock()
    blob1 = MagicMock()
    blob2 = MagicMock()
    blob3 = MagicMock()
    blob1.name = "pages/"
    blob2.name = "pages/charmander"
    blob3.name = "pages/squirtle"
    client.get_bucket.return_value = bucket
    bucket.list_blobs.return_value = [blob1, blob2, blob3]
    backend = Backend(client)
    assert backend.get_all_page_names() == ['pages/charmander', 'pages/squirtle']

"""
def test_get_wiki_page(mock_storage):
    backend = Backend(mock_storage)
    assert backend.get_wiki_page('charmander') == ['Charmander', 'Fire', 'Kanto']


def test_get_all_page_names(mock_storage):
    backend = Backend(mock_storage)
    assert backend.get_all_page_names() == ['pages/charmander', 'pages/squirtle', 'pages/bulbasaur']


def test_sign_up_account_already_exists(mock_storage):
    backend = Backend(mock_storage)
    assert backend.sign_up('javier', 'pokemon123') == False


def test_sign_up_successful(mock_storage, mock_hashfunc):
    backend = Backend(mock_storage, mock_hashfunc)
    assert backend.sign_up('newUser', 'pokemon123') == True


def test_sign_in_account_does_not_exist(mock_storage):
    backend = Backend(mock_storage)
    assert backend.sign_in('newUser', 'guest123') == False


def test_sign_in_successful(mock_storage, mock_hashfunc):
    backend = Backend(mock_storage, mock_hashfunc)
    assert backend.sign_in('javier', 'pokemon123') == True
"""