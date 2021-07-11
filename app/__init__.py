from flask import Flask
from flask.blueprints import Blueprint


def create_app(config="config.py"):

    app = Flask(__name__)

    app.config.from_pyfile(config)

    from app.site.views.login import login_bp
    from app.site.views.works import works_bp
    from app.site.views.employees import employees_bp
    from app.site.views.rescuers import rescuers_bp
    from app.site.views.hazards import hazards_bp
    from app.site.views.paths import paths_bp
    from app.site.views.hotspots import hotspots_bp
    from app.site import site

    site.register_blueprint(login_bp)
    site.register_blueprint(works_bp)
    site.register_blueprint(paths_bp)
    site.register_blueprint(hotspots_bp)
    site.register_blueprint(employees_bp)
    site.register_blueprint(rescuers_bp)
    site.register_blueprint(hazards_bp)

    from app.api.routes import api

    app.register_blueprint(site)
    app.register_blueprint(api)

    return app
