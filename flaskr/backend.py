# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import base64
from flask import json

AUTHENTICATED_URL = "https://storage.cloud.google.com/wiki-content-techx/poke_imgs/"

class Backend:
    
    def __init__(self):
        self.client = storage.Client()
        
    def get_wiki_page(self, name, bucket_name):
        pass

    def get_all_page_names(self):
        blobs = self.client.list_blobs("wiki-content-techx", prefix="pokemon/" )
        page_names = []
        for blob in blobs:
            name = blob.name
            page_names.append(blob.name)
        return page_names

    def upload(self, file, pokemon_dict ):
        bucket = self.client.get_bucket('wiki-content-techx')
    
        # image upload
        img_blob = bucket.blob('poke_imgs/' + file.filename)
        img_blob.upload_from_file(file)

        # add image url to pokemon dictionary and turn into json object
        img_url = AUTHENTICATED_URL + file.filename
        pokemon_dict["img_url"] = img_url
        json_obj = json.dumps( pokemon_dict )

        # json object upload
        json_blob = bucket.blob('pokemon/' + pokemon_dict["name"])
        json_blob.upload_from_string(data=json_obj, content_type="application/json")
        
    def sign_up(self):
        bucket = self.client.get_bucket('users-passwords-techx')
        
    def sign_in(self):
        bucket = self.client.get_bucket('users-passwords-techx')

    def get_image(self, blob_name):
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.get_blob(blob_name)
        with blob.open('rb') as f:
            content = f.read()
        image = base64.b64encode(content).decode("utf-8")
        return image


backend = Backend()
backend.get_image('authors/edgar.png')