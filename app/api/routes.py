import os
from flask import Blueprint, request, jsonify, abort, send_file, current_app
from werkzeug.utils import secure_filename
from flask_jwt import jwt
from functools import wraps

from app.utils.dbconnect import select, select_all, commit
from app.api.dijkstra import pathFinder

api = Blueprint("api", __name__, url_prefix="/api")


def token_required(func):
    @wraps(func)
    def warpper(*args, **kwargs):
        auth_header = request.headers.get("authorization")
        if not auth_header:
            abort(401, "missing authorization header")

        token = auth_header.split(" ")[1]
        try:
            secret = current_app.config["SECRET_KEY"]
            user = jwt.decode(jwt=token, key=secret)
        except Exception as e:
            print(e)
            abort(401, "invalid token")

        return func(*args, **kwargs)

    return warpper


# login endpoint
@api.route("/login", methods=["POST"])
def login():

    args = request.get_json()

    # validate login
    if request.method == "POST":
        try:
            username = args["username"]
            password = args["password"]

            query = """SELECT user_id, username, user_type FROM login
                WHERE username=%s AND password=%s"""
            result = select(query, username, password)

            if result is not None:
                payload = result
                secret = current_app.config["SECRET_KEY"]
                token = jwt.encode(payload=payload, key=secret)

                return jsonify(ok=True, token=token.decode("UTF-8")), 200

            else:
                return jsonify(ok=False, message="invalid credentials"), 200

        except Exception as e:
            print(e)
            return jsonify(ok=False), 500


# hazard reports endpoint
@api.route("/hazards", methods=["POST", "GET", "PATCH"])
@token_required
def hazards():

    args = request.get_json()

    # return all hazard reports
    if request.method == "GET":
        try:
            query = """SELECT h_id,username,landmark,datetime,status FROM login l JOIN hazard_report h
                on(l.user_id = h.user_id)join wifi_settings w on(h.wifi_id = w.wifi_id) ORDER BY datetime DESC"""
            result = select_all(query)
            return jsonify(ok=True, hazards=result), 200

        except Exception as e:
            print(e)
            return jsonify(ok=False), 500

    # add a new hazard report
    if request.method == "POST":

        try:
            user_id = args["user_id"]
            wifi_id = args["wifi_id"]

            query = """INSERT INTO hazard_report
            (user_id,wifi_id,datetime,status) VALUES (%s,%s,NOW(), 'emergency reported')"""

            result = commit(query, user_id, wifi_id)
            return jsonify(ok=True), 200
        except Exception as e:
            print(e)
            return jsonify(ok=False), 500

    # update the status of a hazard
    if request.method == "PATCH":
        try:
            hazard_id = args["hazard_id"]
            status = args["status"]

            query = """UPDATE hazard_report SET status=%s WHERE h_id=%s"""

            result = commit(query, status, hazard_id)
            return jsonify(ok=True), 200
        except Exception as e:
            print(e)
            return jsonify(ok=False), 500


# work assignments endpoint
@api.route("/works", methods=["GET"])
@token_required
def works():

    # return all work assignments of a specific user
    if request.method == "GET":
        try:
            user_id = request.args.get("id")

            query = """SELECT w.* FROM works w join employee e on(w.e_id=e.e_id) WHERE e.user_id=%s
                ORDER BY w.date_assign DESC"""

            result = select_all(query, user_id)

            return jsonify(ok=True, works=result)
        except Exception as e:
            print(e)
            return jsonify(ok=False)


# work and report file handling endpoint
@api.route("/files", methods=["POST", "GET"])
@token_required
def handle_file():

    # download work assignment
    if request.method == "GET":
        try:
            work_id = request.args.get("id")
            if not work_id:
                raise Exception("request arguments not satisfied")
        except Exception as e:
            print(e)
            abort(400)

        try:
            query = """SELECT filename FROM works WHERE w_id=%s"""
            result = select(query, work_id)
            filename = result["filename"]
            WORKS_DIR = current_app.config["WORK_FILES_DIR"]

            return send_file(WORKS_DIR + "/" + filename), 200

        except Exception as e:
            print(e)
            return jsonify(ok=False)

    # upload work report to specific work
    if request.method == "POST":

        try:
            work_id = request.form["work_id"]
            report = request.files["report"]
            if not work_id or not report:
                raise Exception("request arguments not satisfied")
        except Exception as e:
            print(e)
            abort(400)

        try:
            filename = secure_filename(report.filename)
            REPORTS_DIR = current_app.config["REPORT_FILES_DIR"]
            report.save(os.path.join(REPORTS_DIR, filename))
            report.close()

            query = """UPDATE works SET report=%s, date_submit=CURDATE(), status='finished' WHERE w_id=%s"""
            result = commit(query, filename, work_id)
            return jsonify(ok=True), 200

        except Exception as e:
            print(e)
            return jsonify(ok=False), 500


# wifi-settings endpoint
@api.route("/wifi", methods=["GET"])
@token_required
def wifi():

    # return all wifi hotspost info
    if request.method == "GET":
        try:
            query = """SELECT * FROM wifi_settings"""

            result = select_all(query)

            return jsonify(ok=True, hotspots=result)
        except Exception as e:
            print(e)
            return jsonify(ok=False)


# paths endpoint
@api.route("/paths", methods=["GET"])
@token_required
def paths():

    # return the shortest route from a specific source and destination
    if request.method == "GET":

        try:
            nearby_macs = request.args.get("nearby_macs")
            destination_mac = request.args.get("destination")
            if nearby_macs is None or destination_mac is None:
                raise Exception("request arguments not satisfied")
        except Exception as e:
            print(e)
            abort(400)

        try:
            nearby_macs = nearby_macs.split("#")
            source = ""
            source_id = ""

            qry = """SELECT wifi_id, landmark FROM wifi_settings WHERE mac_address = %s """

            for mac in nearby_macs:
                result = select(qry, mac)
                if result is not None:
                    source_id = str(result["wifi_id"])
                    source = str(result["landmark"])
                    break

            print(nearby_macs)
            if source == "":
                return jsonify(ok=False)

            result = select(qry, destination_mac)
            destination_id = str(result["wifi_id"])
            destination = result["landmark"]

            if source == destination:
                return jsonify(ok=True, paths=[])

            else:
                qry = """SELECT wifi_id FROM wifi_settings WHERE landmark = %s """
                result = select(qry, destination)
                destination_id = str(result["wifi_id"])

                pf = pathFinder()
                path_nodes = pf.find_path(source_id, destination_id)

                query = """ SELECT direction, w.landmark as next_stop  FROM paths p
                    JOIN wifi_settings w on (p.landmark_B = w.wifi_id)
                    WHERE p.landmark_A=%s AND p.landmark_B=%s """

                paths = []
                for i in range(0, len(path_nodes) - 1):
                    result = select(query, str(path_nodes[i]), str(path_nodes[i + 1]))
                    paths.append(result)

                print(paths)
                return jsonify(ok=True, paths=paths)

        except Exception as e:
            print(e)
            return jsonify(ok=False)
