import os
from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from app import database
from .constants import ONE
from .auth import auth
from .codes import codes
from .reader import reader

def create_app():
    load_dotenv()
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.secret_key = os.environ.get('SECRET_KEY')
    app.register_blueprint(auth)
    app.register_blueprint(codes)
    app.register_blueprint(reader)
    with app.app_context():
        user = database.execute("SELECT * FROM user LIMIT 1", ONE, [], "")
        if not user:
            myusername = os.getenv("DEFAULT_USERNAME", "root")
            mypassword = os.getenv("DEFAULT_PASSWORD", "root")
            database.execute("CALL create_new_user(%s, %s)", None, [myusername, generate_password_hash(mypassword)], "")
    @app.before_request
    def check_auth():
        if request.endpoint in ['static', 'reader.index', 'auth.index', 'auth.store']:
            return
        if 'userid' not in session:
            return redirect(url_for('auth.index'))
    return app