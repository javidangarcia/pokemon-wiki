# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
import base64

class Backend:
    
    def __init__(self):
        self.client = storage.Client()
        
    def get_wiki_page(self, name, bucket_name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file):
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.blob('poke_imgs/' + file.filename)
        blob.upload_from_file(file)
        
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