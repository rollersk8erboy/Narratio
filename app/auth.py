from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app import database
from app.constants import ONE

auth = Blueprint('auth', __name__)

@auth.route("/auth")
def index():
    if 'userid' in session:
        return redirect(url_for('codes.index'))
    return render_template("auth/index.html")

@auth.route("/auth/store", methods=["POST"])
def store():
    myusername = request.form.get('myusername')
    mypassword = request.form.get('mypassword')
    user = database.execute("CALL get_a_user_by_username(%s)", ONE, [myusername], "")
    if user and check_password_hash(user['password'], mypassword):
        session.clear()
        session['userid'] = user['userid']
        return redirect(url_for('codes.index'))
    flash("La contraseña no es correcta. Compruébala.")
    return redirect(url_for('auth.index'))

@auth.route("/auth/destroy")
def destroy():
    session.clear()
    return redirect(url_for('auth.index'))