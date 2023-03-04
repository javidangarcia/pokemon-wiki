from flaskr.backend import Backend
import pytest

class MockStorageClient():
    def __init__(self):
        pass

    def get_bucket(self, bucket_name):
        bucket = MockBucket()
        return bucket

class MockBucket():
    def __init__(self):
        pass

    def get_blob(self, blob_name):
        blob = MockBlob()
        return blob

class MockBlob():
    def __init__(self):
        pass

    def open(self, mode):
        return self

    def read(self):
        return "Test"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def test_get_wiki_page():
    mock_storage = MockStorageClient()
    backend = Backend(mock_storage)
    assert backend.get_wiki_page('test') == "Test"


