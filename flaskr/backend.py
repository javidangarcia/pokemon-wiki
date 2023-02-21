# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:

    def __init__(self):
        self.client = storage.Client()
        
    def get_wiki_page(self, name, bucket_name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self, file, bucket):
        bucket = self.client.get_bucket(bucket)
        blob = bucket.blob('pokemon/' + file.filename)
        blob.upload_from_file(file)
        
    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

