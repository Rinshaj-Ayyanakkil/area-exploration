from flask import Blueprint, render_template, redirect, request, url_for
from app.site.views.login import login_required

from app.utils.dbconnect import select_all, commit

hazards_bp = Blueprint("hazards", __name__, url_prefix="/hazards")


# render hazard reports page
@hazards_bp.route("/")
@login_required
def hazards(user):

    query = """SELECT l.username,w.landmark,h.h_id,h.datetime,h.status FROM hazard_report h
        JOIN login l ON l.user_id=h.user_id
        JOIN wifi_settings w ON h.wifi_id=w.wifi_id ORDER BY h.datetime DESC"""
    hazards = select_all(query)

    return render_template("view-hazard-reports.html", hazards=hazards, user=user)


# function to update emergency status
@hazards_bp.route("/update", methods=["GET", "POST"])
@login_required
def update_hazard(user):

    h_id = request.args.get("id")
    status = request.args.get("status")

    if request.method == "GET":

        query = """UPDATE hazard_report SET status=%s WHERE h_id=%s"""
        commit(query, status, h_id)

        return redirect(url_for("site.hazards.hazards"))


@hazards_bp.route("/delete")
@login_required
def delete_hazard(user):

    h_id = request.args.get("id")

    query = """DELETE FROM hazard_report WHERE h_id=%s"""
    commit(query, h_id)

    return redirect(url_for("site.hazards.hazards"))
