from flask import Blueprint, render_template, redirect, request, url_for
from app.site.views.login import login_required
from app.utils.dbconnect import select, select_all, commit


import smtplib
from email.mime.text import MIMEText

employees_bp = Blueprint("employees", __name__, url_prefix="/employees")


# render employee management page
@employees_bp.route("/")
@login_required
def employees(user):

    query = "SELECT * FROM employee"
    employees = select_all(query)
    return render_template("view-employees.html", employees=employees, user=employees)


# def send_mail(username, password, email):
#
#         gmail = smtplib.SMTP("smtp.gmail.com", 587)
#         gmail.ehlo()
#         gmail.starttls()
#         gmail.login("smart123.parking@gmail.com", "123.parking")
#     except Exception as e:
#         print("Couldn't setup email!!" + str(e))

#     msg = MIMEText("Your USERNAME :" + username + " and  PASSWORD:" + password)
#     msg["Subject"] = "Employee Login Credentials  "
#     msg["To"] = email
#     msg["From"] = "smart123.parking@gmail.com"
#
#         gmail.send_message(msg)
#         return True
#     except Exception as e:
#         print("COULDN'T SEND EMAIL", str(e))
#         return False


# render page to add a new employee
@employees_bp.route("/register", methods=["GET", "POST"])
@login_required
def add_employee(user):

    if request.method == "GET":

        return render_template("register-employee.html", user=user)

    if request.method == "POST":

        firstName = request.form["addFirstName"]
        lastName = request.form["addLastName"]
        dob = request.form["addAge"]
        gender = request.form["addGender"]
        phone = request.form["addPhone"]
        email = request.form["addEmail"]
        place = request.form["addPlace"]
        post = request.form["addPost"]
        pin = request.form["addPin"]
        username = request.form["addUsername"]
        password = request.form["addPassword"]

        query = """INSERT INTO login(username,password,user_type) VALUES(%s,%s,'employee')"""
        user_id = commit(query, username, password)

        query = """INSERT INTO employee(first_name,last_name,dob,gender,phone,email,place,post,pin,user_id) 
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        commit(query, firstName, lastName, dob, gender, phone, email, place, post, pin, user_id)

        return redirect(url_for("site.employees.employees"))

        # return """<script>alert('Employee Added Successfully');window.location='/view-employees'</script>"""


# render page to edit an employee
@employees_bp.route("/edit", methods=["GET", "POST"])
@login_required
def edit_employee(user):

    e_id = request.args.get("id")

    if request.method == "GET":

        query = "SELECT * FROM employee WHERE e_id=%s"
        employee = select(query, e_id)

        return render_template("edit-employee.html", user=user, employee=employee)

    if request.method == "POST":

        firstname = request.form["firstName"]
        lastname = request.form["lastName"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        phone = request.form["phone"]
        email = request.form["email"]
        place = request.form["place"]
        post = request.form["post"]
        pin = request.form["pin"]

        query = """UPDATE employee 
                SET first_name=%s,last_name=%s,dob=%s,gender=%s,phone=%s,email=%s,place=%s,post=%s,pin=%s
                WHERE e_id=%s """
        commit(query, firstname, lastname, dob, gender, phone, email, place, post, pin, e_id)

        return redirect(url_for("site.employees.employees"))


# function for deleting an employee
@employees_bp.route("/delete")
@login_required
def delete_employee(user):

    e_id = request.args.get("id")

    query = "SELECT user_id FROM employee WHERE e_id = %s" ""
    result = select(query, e_id)
    user_id = result["user_id"]

    query = "DELETE FROM login WHERE user_id=%s"
    commit(query, user_id)

    return redirect(url_for("site.employees.employees"))
