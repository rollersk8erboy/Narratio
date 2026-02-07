from flask import Blueprint, render_template

reader = Blueprint('reader', __name__)

@reader.route("/reader")
def index():
    return render_template("reader/index.html")
