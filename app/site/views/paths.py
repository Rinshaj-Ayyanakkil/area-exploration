from flask import Blueprint, render_template, redirect, request, url_for
from app.site.views.login import login_required
from app.utils.dbconnect import select_all, commit


paths_bp = Blueprint("paths", __name__, url_prefix="/paths")

# render route allocation page
@paths_bp.route("/")
@login_required
def routes_page(user):

    query = """SELECT w1.landmark as source, w2.landmark as destination, direction FROM paths p 
            JOIN wifi_settings w1 on(p.landmark_A = w1.wifi_id) 
            JOIN wifi_settings w2 on (p.landmark_B = w2.wifi_id)"""
    paths = select_all(query)

    query = "SELECT * FROM wifi_settings"
    hotspots = select_all(query)

    return render_template("view-routes.html", user=user, paths=paths, hotspots=hotspots)
