import os
from flask import Blueprint, render_template, redirect, request, url_for, abort, send_file
from werkzeug.utils import secure_filename
from app.site.views.login import login_required
from app.utils.dbconnect import select, select_all, commit


works_bp = Blueprint("works", __name__, url_prefix="/works")

WORK_FILES_DIR = (
    "/home/rinshaj/programming/Project_Backup_22-06-2021/Project/Backups/areaExploration/app/sites/static/works"
)

# render work assignments page
@works_bp.route("/")
@login_required
def works(user):

    query = """SELECT w.*, e.first_name,e.last_name FROM works w 
        JOIN employee e on w.e_id=e.e_id"""
    works = select_all(query)

    return render_template("view-work-assignments.html", works=works, user=user)


@works_bp.route("/files/<string:filename>")
@login_required
def work_file(user, filename):
    return send_file(WORK_FILES_DIR + "/" + filename), 200


@works_bp.route("/register", methods=["GET", "POST"])
@login_required
def add_work(user):

    if request.method == "GET":

        query = "SELECT e_id,first_name,last_name FROM employee"
        employees = select_all(query)

        return render_template("assign-new-work.html", employees=employees, user=user)

    if request.method == "POST":

        try:
            e_id = request.form["employee"]
            work_name = request.form["work_name"]
            deadline = request.form["deadline"]
            work_file = request.files["work_file"]

            filename = secure_filename(work_file.filename)
            work_file.save(os.path.join(WORK_FILES_DIR, filename))

            query = """INSERT INTO works(e_id,work_name,filename,deadline,date_assign,status)
                    VALUES(%s,%s,%s,%s,CURDATE(),'pending') """
            commit(query, e_id, work_name, filename, deadline)
        except Exception as e:
            print(e)
            abort(500)

        return redirect(url_for("site.works.works"))


# function to cancel a work assignment
@works_bp.route("/delete")
@login_required
def delete_work(user):

    work_id = request.args.get("id")

    query = """DELETE FROM works WHERE w_id=%s"""
    commit(query, work_id)

    return redirect(url_for("site.works.works"))


# render work reports page
@works_bp.route("/report")
@login_required
def work_reports_page(user):

    work_id = request.args.get("id")

    query = """SELECT w.*, e.first_name,e.last_name FROM works w 
        JOIN employee e on w.e_id=e.e_id WHERE w.e_id=%s"""
    work = select(query, work_id)
    print(work)

    return render_template("view-work-reports.html", work=work, user=user)
