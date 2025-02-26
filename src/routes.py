from flask import Blueprint, render_template

main_routes = Blueprint("main_routes", __name__)  # Ensure this matches url_for()

@main_routes.route("/")
def home():
    return render_template("index.html")
