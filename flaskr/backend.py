from google.cloud import storage
import base64
import hashlib

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
        
    def sign_up(self, username, password):
        bucket = self.client.get_bucket('users-passwords-techx')
        blob = bucket.blob(username)

        # salting the password with username and a secret word
        salt = f"{username}{jmepokemon}{password}"
        # generating hashed password after the salting
        hashed_password = hashlib.blake2b(salt.encode()).hexdigest()

        # writing hashed password to the new user blob we created
        with blob.open('w') as f:
            f.write(hashed_password)
        
    def sign_in(self, username, password):
        # salting the password with username and a secret word
        salt = f"{username}{jmepokemon}{password}"
        # generating hashed password after the salting
        hashed_password = hashlib.blake2b(salt.encode()).hexdigest()

        bucket = self.client.get_bucket('users-passwords-techx')
        blob = bucket.get_blob(username)

        # reading hashed password from the username
        with blob.open('r') as f:
            content = f.read()

        # checking whether the hashed password matches the password given
        if content == hashed_password:
            return True
        else: return False

    def get_image(self, blob_name):
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.get_blob(blob_name)
        with blob.open('rb') as f:
            content = f.read()
        image = base64.b64encode(content).decode("utf-8")
        return image


# Typical Usage (SignUp & SignIn):
# backend = Backend()
# backend.sign_up('javiergarcia', 'pokemon123')
# backend.sign_in('javiergarcia', 'poke525') # should return False because it doesn't match password in cloud storage
# backend.sign_in('javiergarcia', 'pokemon123') # should return True and sign the user in