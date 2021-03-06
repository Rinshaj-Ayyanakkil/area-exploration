import pymysql
from flask import current_app


def getConnection():
    with current_app.app_context():
        HOST = current_app.config["DB_HOST"]
        PORT = int(current_app.config["DB_PORT"])
        USER = current_app.config["DB_USER"]
        PASSWORD = current_app.config["DB_PASSWORD"]
        DB = current_app.config["DB_NAME"]
        connection = pymysql.connect(
            host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, cursorclass=pymysql.cursors.DictCursor
        )
        return connection


# function for fetching a single row
def select(qry, *params):
    connection = getConnection()
    cursor = connection.cursor()  # creating a cursor object
    cursor.execute(qry, (params))  # execute the query
    result: dict = cursor.fetchone()  # fetching a single row of query result
    connection.close()  # closing connection
    return result  # returning the query result


# function for fetching entire result
def select_all(qry, *params):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute(qry, (params))
    result: dict = cursor.fetchall()  # fetching entire result
    connection.close()
    return result


# function to insert/update/delete/alter the data in database
def commit(qry, *params):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute(qry, (params))
    connection.commit()  # committing the changes made to the database
    last_row_id = cursor.lastrowid  # return the value generated by auto-increment constraint
    connection.close()
    return last_row_id
