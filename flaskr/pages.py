from flask import render_template,request
from .backend import Backend
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


def make_endpoints(app):

    class LoginForm(FlaskForm):
        username = StringField('Username', [validators.InputRequired()], render_kw={"placeholder":"Username"})
        password = PasswordField('Password', [validators.InputRequired()], render_kw={"placeholder":"Password"})
        submit = SubmitField('Login')

    class SignupForm(FlaskForm):
        username = StringField([validators.InputRequired()], render_kw={"placeholder":"Username"})
        password = PasswordField('Password', [validators.InputRequired()], render_kw={"placeholder":"Password"})
        submit = SubmitField('Signup')

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
        backend = Backend()
        images = [backend.get_image('authors/javier.png'), backend.get_image('authors/edgar.png'), backend.get_image('authors/mark.png')]
        return render_template('about.html', content_type='image/png', images=images)

    @app.route("/pages")
    def pages():
        return render_template('pages.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        # User validation

        return render_template('login.html', form=form)

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        form = SignupForm()
        # User validation

        return render_template('signup.html', form=form)

    @app.route("/upload")
    def upload():
        return render_template("upload.html")
    
    @app.route("/upload",methods=["POST"])
    def upload_file():
        name = request.form["name"]
        
        file_to_upload = request.files['file']
        backend = Backend()
        backend.upload(file_to_upload, json_to_upload)
        return render_template("main.html")