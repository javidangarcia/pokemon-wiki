from flaskr.backend import Backend
import pytest
from unittest.mock import MagicMock, patch


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


@pytest.fixture
def base64func():
    return MagicMock()


@pytest.fixture
def imagefile():
    return MagicMock()


@pytest.fixture
def mockjson():
    return MagicMock()


def test_get_wiki_page(client, bucket, blob, file):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.open.return_value.__enter__.return_value = file
    file.read.return_value = ['Charmander', 'Fire', 'Kanto']
    backend = Backend(client)
    assert backend.get_wiki_page('charmander') == [
        'Charmander', 'Fire', 'Kanto'
    ]


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
    assert backend.get_all_page_names() == [
        'pages/charmander', 'pages/squirtle'
    ]


def test_upload_successful(client, bucket, blob, base64func, imagefile,
                           mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = None
    bucket.blob.return_value = blob
    imagefile.filename = "charmander.png"
    imagefile.content_type = "image/png"
    backend = Backend(client, hashfunc, base64func, mockjson)
    pokemon_data = {"name": "Charmander"}
    assert backend.upload(imagefile, pokemon_data) == True
    assert pokemon_data["image-name"] == "charmander.png"
    assert pokemon_data["image-type"] == "image/png"


def test_upload_page_already_exists(client, bucket, blob, imagefile):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    backend = Backend(client)
    pokemon_data = {"name": "Charmander"}
    assert backend.upload(imagefile, pokemon_data) == False


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
    assert backend.sign_in('javier', 'pokemon123') == True


def test_get_image(client, bucket, blob, file, hashfunc, base64func):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.open.return_value.__enter__.return_value = file
    file.read.return_value = "\x00\x08\x00\x00\x00\x06\x00\x12\x01\x03"
    base64func.b64encode.return_value.decode.return_value = "YSqYWCEU3S9RsqUCGlwfUtQTkcpzLxM4pS3Pj1A"
    backend = Backend(client, hashfunc, base64func)
    assert backend.get_image(
        'charmander') == "YSqYWCEU3S9RsqUCGlwfUtQTkcpzLxM4pS3Pj1A"


"""
Unit Tests for New Backend Features
"""

def test_get_pages_by_search(client, bucket, mockjson):
    blobs = [MagicMock() for i in range(2)]
    blobs[0].name = "pages/"
    blobs[1].name = "pages/charmander"
    json_obj = {"name": "charmander"}
    client.get_bucket.return_value = bucket
    bucket.list_blobs.return_value = iter(blobs)
    mockjson.loads.return_value = json_obj
    backend = backend = Backend(client, json=mockjson)
    assert backend.get_pages_using_search("char") == ["pages/charmander"]

def test_get_leaderboard(client, bucket, blob, mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.download_as_string.return_value = ""
    data = ["name1", "name2", "name3"]
    mockjson.loads.return_value = {"ranks_list": data}
    backend = Backend(client, json=mockjson)
    assert backend.get_leaderboard() == data 

def test_get_pokemon_image(client,bucket,blob,base64func,imagefile):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    pokemon_image_blob = bucket.get_blob()
    pokemon_image_blob.open.return_value.__enter__.return_value = imagefile
    imagefile.read.return_value = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    base64func.b64encode.return_value.decode.return_value = "DlqDRdKbrjQdWsQEjhVV"
    backend = Backend(client,base64func=base64func)
    assert backend.get_pokemon_image(3) == "DlqDRdKbrjQdWsQEjhVV"

def test_get_pokeball(client,bucket,blob,base64func,imagefile):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    pokeball_blob = bucket.get_blob()
    pokeball_blob.open.return_value.__enter__.return_value = imagefile
    imagefile.read.return_value = "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20"
    base64func.b64encode.return_value.decode.return_value = "xpMlfYxxbIZKvEPCNVZx"
    backend = Backend(client,base64func=base64func)
    assert backend.get_pokeball() == "xpMlfYxxbIZKvEPCNVZx"


@patch("flaskr.backend.Backend.get_game_user",
       return_value={"User": 1})
@patch("flaskr.backend.Backend.update_leaderboard",
       return_value=b"new leaderboard")
def test_update_points(game_user,leaderboard,client,bucket,blob,mockjson):
    client.get_bucket.return_value = bucket
    bucket.blob.return_value = blob
    mockjson.dumps.return_value = {"edgar":1}
    backend = Backend(client,json=mockjson)
    backend.update_points("username",{"edgar":1})
    game_user.assert_called_once()
    leaderboard.assert_called_once()
    blob.upload_from_string.assert_called_once_with(data={"edgar":1},content_type="application/json")

def test_get_pokemon_data(client,bucket,blob,mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.download_as_string.return_value = "downloaded string"
    mockjson.loads.return_value = {1:"abra"}
    backend = Backend(client,json=mockjson)
    assert backend.get_pokemon_data(2) == "abra"

def test_get_seen_pokemon(client,bucket,blob,mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.download_as_string.return_value = "A string"
    mockjson.loads.return_value = {"100":"true","200":"true"}
    backend = Backend(client,json=mockjson)
    assert backend.get_seen_pokemon("username") == {"100":"true","200":"true"}


def test_update_seen_pokemon(client,bucket,blob,mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    mockjson.dumps.return_value = {"new":"pokemon"}
    backend = Backend(client,json=mockjson)
    backend.update_seen_pokemon("username",{"new":"list"})
    blob.upload_from_string.assert_called_once


def test_get_game_user(client, bucket, blob, mockjson):
    client.get_bucket.return_value = bucket
    bucket.get_blob.return_value = blob
    blob.download_as_string.return_value = ""
    data = {"name": "name", "points": 0, "rank": None}
    mockjson.loads.return_value = data
    backend = Backend(client, json=mockjson)
    assert backend.get_game_user("name") == data

@patch("flaskr.backend.Backend.get_leaderboard", return_value=[])
def test_update_leaderboard_unranked_user(client, bucket, blob, mockjson):
    client.get_bucket.return_value = bucket
    bucket.blob.return_value = blob
    mockjson.dumps.return_value = ""
    data = {"name": "name", "points": 0, "rank": None}
    backend = Backend(client, json=mockjson)
    assert backend.update_leaderboard(data) == {"name": "name", "points": 0, "rank": 1}

@patch("flaskr.backend.Backend.get_leaderboard", return_value=[{"name": "name", "points": 0, "rank": 1}])
def test_update_leaderboard_only_user(client, bucket, blob, mockjson):
    client.get_bucket.return_value = bucket
    bucket.blob.return_value = blob
    mockjson.dumps.return_value = ""
    data = {"name": "name", "points": 100, "rank": 1}
    backend = Backend(client, json=mockjson)
    assert backend.update_leaderboard(data) == {"name": "name", "points": 100, "rank": 1}

@patch("flaskr.backend.Backend.get_leaderboard", 
    return_value=[{"name": "name", "points": 100, "rank": 1}, {"name": "name2", "points": 0, "rank": 2}])
@patch("flaskr.backend.Backend.sort_leaderboard",
    return_value=([{"name": "name2", "points": 200, "rank": 1}, {"name": "name", "points": 100, "rank": 2}], {"name": "name2", "points": 200, "rank": 1}))
def test_update_leaderboard(client, bucket, blob, mockjson):
    client.get_bucket.return_value = bucket
    bucket.blob.return_value = blob
    mockjson.dumps.return_value = ""
    data = {"name": "name2", "points": 200, "rank": 2}
    backend = Backend(client, json=mockjson)
    assert backend.update_leaderboard(data) == {"name": "name2", "points": 200, "rank": 1}

def test_sort_up_leaderboard(client):
    backend = Backend(client)
    data = [{"name": "name", "points": 100, "rank": 1}, {"name": "name2", "points": 0, "rank": 2}]
    user_data = {"name": "name2", "points": 200, "rank": 2}
    assert backend.sort_leaderboard(data, user_data) == ([{"name": "name2", "points": 200, "rank": 1}, {"name": "name", "points": 100, "rank": 2}], 
                                                        {"name": "name2", "points": 200, "rank": 1})

def test_sort_down_leaderboard(client):
    backend = Backend(client)
    data = [{"name": "name", "points": 100, "rank": 1}, {"name": "name2", "points": 100, "rank": 2}]
    user_data = {"name": "name", "points": 50, "rank": 1}
    assert backend.sort_leaderboard(data, user_data) == ([{"name": "name2", "points": 100, "rank": 1}, {"name": "name", "points": 50, "rank": 2}], 
                                                        {"name": "name", "points": 50, "rank": 2})

def test_sort_leaderboard_equal_points(client):
    backend = Backend(client)
    data = [{"name": "name", "points": 100, "rank": 1}, {"name": "name2", "points": 0, "rank": 2}]
    user_data = {"name": "name2", "points": 100, "rank": 2}
    assert backend.sort_leaderboard(data, user_data) == ([{"name": "name", "points": 100, "rank": 1}, {"name": "name2", "points": 100, "rank": 2}],
                                                        {"name": "name2", "points": 100, "rank": 2})