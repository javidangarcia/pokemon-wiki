# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
class Backend:

    def __init__(self):
        self.client = storage.Client()
        
        
        
    def get_wiki_page(self, name, bucket_name):
        pass

    def get_all_page_names(self):
        pass

    def upload(self,file_to_upload,bucket_name):
        bucket = self.client.get_bucket(bucket_name)
        object_to_be_stored = bucket.blob(file_to_upload.filename)
        object_to_be_stored.upload_from_file( file_to_upload )
        

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass

