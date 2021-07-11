from flask import Blueprint

site = Blueprint("site", __name__, static_folder="static", static_url_path="/site/static", template_folder="templates")
