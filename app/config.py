import os

# session secret key
SECRET_KEY = os.environ.get("SECRET_KEY")

# upload folders
REPORT_FILES_DIR = "site/static/uploads/reports"
WORK_FILES_DIR = "site/static/uploads/works"

# database variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
