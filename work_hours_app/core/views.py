from flask import render_template, request, Blueprint

core = Blueprint("core", __name__)

@core.route("/")
def index():
    return render_template("core/index.html")
