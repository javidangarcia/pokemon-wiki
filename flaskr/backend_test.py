from flaskr.backend import Backend
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def client():
    return MagicMock()

@pytest.fixture
def bucket():
    return MagicMock()

@pytest.fixture
def blob():
    return MagicMock()

@pytest.fixture
def file():
    return MagicMock()

@pytest.fixture
def hashfunc():
    return MagicMock()


def test_get_wiki_page(client, bucket, blob, file):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.open.return_value.__enter__.return_value = file
    file.read.return_value = ['Charmander', 'Fire', 'Kanto']
    backend = Backend(client)
    assert backend.get_wiki_page('charmander') == ['Charmander', 'Fire', 'Kanto']


def test_get_all_page_names(client, bucket):
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


def test_upload(client, bucket):
    client.get_bucket.return_value = bucket
    


def test_sign_up_account_already_exists(client, bucket, blob):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    backend = Backend(client)
    assert backend.sign_up('javier', 'pokemon123') == False


def test_sign_up_successful(client, bucket, blob, file, hashfunc):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = None
    bucket.blob.return_value = blob
    hashfunc.blake2b.return_value.hexdigest.return_value = "pokemon123" 
    blob.open.return_value.__enter__.return_value = file
    backend = Backend(client, hashfunc)
    assert backend.sign_up('newUser', 'pokemon123') == True


def test_sign_in_account_does_not_exist(client, bucket):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = None
    backend = Backend(client)
    assert backend.sign_in('newUser', 'pokemon123') == False


def test_sign_in_successful(client, bucket, blob, file, hashfunc):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    hashfunc.blake2b.return_value.hexdigest.return_value = "pokemon123" 
    blob.open.return_value.__enter__.return_value = file
    file.read.return_value = "pokemon123"
    backend = Backend(client, hashfunc)
    assert backend.sign_in('newUser', 'pokemon123') == True