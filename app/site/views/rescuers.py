from flask import Blueprint, render_template, redirect, request, url_for
from app.site.views.login import login_required
from app.utils.dbconnect import select, select_all, commit


rescuers_bp = Blueprint("rescuers", __name__, url_prefix="/rescuers")

# render rescuer management page
@rescuers_bp.route("/")
@login_required
def rescuers(user):

    query = "SELECT * FROM rescuer"
    rescuers = select_all(query)
    return render_template("view-rescuers.html", rescuers=rescuers, user=user)


# render the page to add new rescuers
@rescuers_bp.route("/register", methods=["GET", "POST"])
@login_required
def add_rescuer(user):

    if request.method == "GET":

        return render_template("register-rescuer.html", user=user)

    if request.method == "POST":

        unit_name = request.form["unitName"]
        contact = request.form["contact"]
        username = request.form["username"]
        password = request.form["password"]

        query = """INSERT INTO login(username,password,user_type) VALUES(%s,%s,'rescuer')"""
        user_id = commit(query, username, password)

        query = """INSERT INTO rescuer(unit_name,contact,user_id) 
                VALUES(%s,%s,%s) """
        commit(query, unit_name, contact, user_id)

        return redirect(url_for("site.rescuers.rescuers"))
        # return """<script>alert('Rescuer Added Successfully');window.location='/view-rescuers'</script>"""


# render page to edit an rescuer
@rescuers_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_rescuer(user):

    unit_id = request.args.get("id")

    if request.method == "GET":

        query = """SELECT * FROM rescuer WHERE unit_id=%s"""
        rescuer = select(query, unit_id)

        return render_template("edit-rescuer.html", user=user, rescuer=rescuer)

    if request.method == "POST":

        unit_name = request.form["unitName"]
        contact = request.form["contact"]

        query = """UPDATE rescuer 
                SET unit_name=%s,contact=%s WHERE unit_id=%s """
        commit(query, unit_name, contact, unit_id)

        return redirect(url_for("site.rescuers.rescuers"))


# function to delete a rescuer
@rescuers_bp.route("/delete")
@login_required
def delete_rescuer(user):

    unit_id = request.args.get("id")

    query = """SELECT user_id FROM rescuer WHERE unit_id = %s """
    result = select(query, unit_id)
    user_id = result["user_id"]

    query = """DELETE FROM login WHERE user_id=%s"""
    commit(query, user_id)

    return redirect(url_for("site.rescuers.rescuers"))
