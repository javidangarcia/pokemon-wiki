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
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.get_blob('authors/javier.png')
        with blob.open('rb') as f:
            return f.read()




