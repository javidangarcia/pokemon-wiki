from flask import render_template,request
from .backend import Backend


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template('main.html')

    # TODO(Project 1): Implement additional routes according to the project requirements.
    @app.route("/about")
    def about():
        return render_template('about.html')

    @app.route("/pages")
    def pages():
        return render_template('pages.html')

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/upload")
    def upload():
        return render_template("upload.html")
    
    @app.route("/upload",methods=["POST"])
    def upload_file():
        file_to_upload = request.files['file']
        backend = Backend()
        backend.upload(file_to_upload, "wiki-content-techx")
        return render_template("main.html")
