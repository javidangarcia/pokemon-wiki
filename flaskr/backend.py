"""This module contains the backend of the pokemon wiki which interacts with the Google Cloud Storage.
The backend retrieves user generated pages and image data from the cloud, creates username and password blobs, creates hashed passwords,
compares username and password blobs for logging in, and uploads user generated page data to the cloud.

Typical Usage:
backend = Backend()
data = backend.get_wiki_page('charmander')
pages = backend.get_all_page_names()
backend.upload('charmander.png', pokemon_dictionary)
signup = backend.sign_up('javier', 'pokemon123')
login = backend.sign_in('javier', 'pokemon123')
image = get_image('pokemon/charmander')
"""

from google.cloud import storage
import base64
import hashlib
from flask import json, render_template, flash, redirect, url_for
from .user import User
from secrets import randbelow


class Backend:

    def __init__(self,
                 client=storage.Client(),
                 hashfunc=hashlib,
                 base64func=base64,
                 json=json):
        """
        Args:
            client: Dependency injection for mocking the cloud storage client.
            hashfunc: Dependency injection for mocking the hashlib module.
            base64func: Dependency injection for mocking the base64 module.
            json: Dependency injection for mocking the json module.
        """
        self.client = client
        self.hashfunc = hashfunc
        self.base64func = base64func
        self.json = json

    def get_wiki_page(self, name):
        """ Retrieves user generated page from cloud storage and returns it.
        Args:
            name: The name of the user generated page to retrieve from the cloud.
        Returns:
            content: The user generated page data.
        """
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.get_blob(f'pages/{name}')

        # reading json object blob and returning its contents
        with blob.open('r') as f:
            content = f.read()
        return content

    def get_all_page_names(self):
        """ Retrieves the names of all user generated pages and returns a list containing them.
        Returns:
            page_names: List that contains all user generated page names as strings.
        """
        bucket = self.client.get_bucket('wiki-content-techx')
        blobs = bucket.list_blobs(prefix='pages/')
        page_names = []

        # adding every blob to page_names except the first blob since it's just the folder name
        for index, blob in enumerate(blobs):
            if index == 0:
                continue
            page_names.append(blob.name)
        return page_names

    def upload(self, file, pokemon_data):
        """ Uploads image data and user generated page data to the cloud storage.
        Args:
            file: The image file uploaded by the user.
            pokemon_data: A dictionary with all data associated with user generated page.
        """
        bucket = self.client.get_bucket('wiki-content-techx')

        path = 'pages/' + pokemon_data["name"].lower()
        blob = bucket.get_blob(path)

        if not blob:
            # uploading user image of pokemon to the pokemon blob
            pokemon = bucket.blob(f'pokemon/{file.filename}')
            pokemon.upload_from_file(file)

            # adding image data to pokemon dictionary
            with pokemon.open('rb') as f:
                content = f.read()
            image = self.base64func.b64encode(content).decode("utf-8")
            pokemon_data["image"] = image

            # adding image type (jpg, png, etc) to pokemon dictionary
            pokemon_data["image_type"] = file.content_type

            # converting pokemon dictionary to json object
            json_obj = self.json.dumps(pokemon_data)

            # creating a json object blob in the pages blob
            blob = bucket.blob(path)
            blob.upload_from_string(data=json_obj,
                                    content_type="application/json")

            return True

        return False

    def sign_up(self, username, password):
        """ Uploads user account information to the cloud storage if account doesn't already exist.
            Creates a hashed password from user password and uploads new password to cloud storage.
        Args:
            username: The username that the user inputs.
            password: The password that the user inputs.
        """
        bucket = self.client.get_bucket('users-passwords-techx')

        game_users_bucket = self.client.get_bucket('wiki-content-techx')
        path = f'user_game_ranking/game_users/{username}'

        # if an account with that username already exists we shouldn't be creating a new one
        if bucket.get_blob(username):
            return False
        else:
            blob = bucket.blob(username)

            # salting the password with username and a secret word
            salt = f"{username}jmepokemon{password}"
            # generating hashed password after the salting
            hashed_password = self.hashfunc.blake2b(salt.encode()).hexdigest()

            # writing hashed password to the new user blob we created
            with blob.open('w') as f:
                f.write(hashed_password)

            # Adds new user to the ranking blob
            game_blob = game_users_bucket.blob(path)
            json_obj = {"points": 0, "rank": None}
            json_str = self.json.dumps(json_obj)
            game_blob.upload_from_string(data=json_str, content_type="application/json")

            return True

    def sign_in(self, username, password):
        """ Checks whether specific account information exists in the cloud storage.
            Creates a hashed password from user password and compares it with the hashed 
            password associated with the username if it exists.
        Args:
            username: The username that the user inputs.
            password: The password that the user inputs.
        """
        bucket = self.client.get_bucket('users-passwords-techx')
        blob = bucket.get_blob(username)

        if blob:
            # salting the password with username and a secret word
            salt = f"{username}jmepokemon{password}"
            # generating hashed password after the salting
            hashed_password = self.hashfunc.blake2b(salt.encode()).hexdigest()

            # reading hashed password from the username
            with blob.open('r') as f:
                content = f.read()
            # checking whether the hashed password matches the password given
            if content == hashed_password:
                return True

        return False

    def get_image(self, blob_name):
        """ Retrieves image data from cloud storage and converts it to base64.
        Args:
            blob_name: Name of image blob that needs to be retrieved and displayed on website.
        Returns:
            image: Image data converted to base64 for front-end use.
        """
        bucket = self.client.get_bucket('wiki-content-techx')
        blob = bucket.get_blob(blob_name)
        with blob.open('rb') as f:
            content = f.read()
        image = self.base64func.b64encode(content).decode("utf-8")
        return image

    def get_user(self, username):
        """ Creates User object containing username and hashed password retreived from cloud storage.
        Args:
            username: The username that the user inputs.
        Returns:
            User(username, password): User object for account related use.
        """
        bucket = self.client.get_bucket('users-passwords-techx')
        blob = bucket.get_blob(username)

        if blob:
            with blob.open('r') as f:
                password = f.read()
            return User(username, password)
        else:
            return None

    def get_game_user(self, username):
            game_users_bucket = self.client.get_bucket('wiki-content-techx')
            path = f'user_game_ranking/game_users/{username}'

            blob = game_users_bucket.get_blob(path)

            json_str = blob.download_as_string()

            json_obj = self.json.loads(json_str)

            return username, json_obj # Returns tuple