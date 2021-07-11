from flask import Blueprint, render_template, redirect, request, url_for
from app.site.views.login import login_required
from app.utils.dbconnect import select, select_all, commit


hotspots_bp = Blueprint("hotspots", __name__, url_prefix="/hotspots")


# function to render wifi settings page
@hotspots_bp.route("/")
@login_required
def hotspots(user):

    query = """SELECT * FROM wifi_settings"""
    hotspots = select_all(query)
    return render_template("view-wifi-settings.html", hotspots=hotspots, user=user)


# render new wifi page
@hotspots_bp.route("/register", methods=["GET", "POST"])
@login_required
def add_hotspot(user):
    if request.method == "GET":

        return render_template("add-wifi-settings.html", user=user)

    if request.method == "POST":

        mac_address = request.form["wifiSettingsWifi"]
        landmark = request.form["wifiSettingsLandmark"]

        query = """INSERT INTO wifi_settings(mac_address,landmark) VALUES(%s,%s) """
        commit(query, mac_address, landmark)
        # return """<script>alert('Settings Added Successfully');window.location='/wifi-settings'</script>"""
        return redirect(url_for("site.hotspots.hotspots"))


# @hotspots_bp.route("/edit/<string:work_id>", methods=["GET", "POST"])
# @login_required
# def edit_hotspots(user, wifi_id):

#     if request.method == "GET":

#         query = "SELECT * FROM wifi_settings WHERE wifi_id=%s"
#         employee = select(query)

#         return render_template("edit-employee.html", user=user, employee=employee)

#     if request.method == "POST":

#         firstname = request.form["firstName"]
#         lastname = request.form["lastName"]
#         dob = request.form["dob"]
#         gender = request.form["gender"]
#         phone = request.form["phone"]
#         email = request.form["email"]
#         place = request.form["place"]
#         post = request.form["post"]
#         pin = request.form["pin"]

#         query = """UPDATE employee
#                 SET first_name=%s,last_name=%s,dob=%s,gender=%s,phone=%s,email=%s,place=%s,post=%s,pin=%
#                 WHERE e_id=%s """
#         commit(query, firstname, lastname, dob, gender, phone, email, place, post, pin, wifi_id)

#         return redirect(url_for("site.hotspots.hotspots"))


# function to delete a wifi setting
@hotspots_bp.route("/delete")
@login_required
def delete_hotspot(user):

    wifi_id = request.args.get("id")
    qry = """DELETE FROM wifi_settings WHERE wifi_id=%s"""
    commit(qry, wifi_id)

    return redirect(url_for("site.hotspots.hotspots"))
