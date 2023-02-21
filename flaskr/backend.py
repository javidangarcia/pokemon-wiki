# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:
    
    def __init__(self):
        self.client = storage.Client()
        
    def get_wiki_page(self, name, bucket_name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file):
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.blob('pokemon/' + file.filename)
        blob.upload_from_file(file)
        
    def sign_up(self):
        bucket = self.client.get_bucket('users-passwords-techx')
        
    def sign_in(self):
        bucket = self.client.get_bucket('users-passwords-techx')

    def get_image(self):
        bucket = self.client.get_bucket('authors-techx')
        # Just testing some things not the official or correct implementation whatsoever
        blobs = bucket.list_blobs()
        links = []
        for blob in blobs:
            links.append(blob.public_url)
        return links



