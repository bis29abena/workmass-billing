from app import app
import os
from app.task import extract_data
from werkzeug.utils import secure_filename
from flask import render_template, request, send_from_directory, abort, flash, session, redirect, url_for

@app.route("/", methods=["GET", "POST"])
def home():
    message = None
    if request.method == "POST":

        file_ = request.files["file"]

        try:

            filename = secure_filename(file_.filename)
            file_path = os.path.join(app.config["EXTRACTION_FILE_PATH"], filename)
            print(file_path)
            file_.save(file_path)
        except IsADirectoryError:
            flash("Please make sure you select a file", "warning")
            return render_template("index.html", message=message)

        file_path = os.path.join(app.config["EXTRACTION_FILE_PATH"])
        session["TEMP_NAME"] = file_.filename

        extract = extract_data(filepath=file_path, file=file_.filename)
        
        message = extract
        

    return render_template("index.html", message=message)

@app.route("/download/<file>")
def download_template(file):
    try:
        return send_from_directory(app.config["TEMPLATE_FILE_PATH"], file, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/download_extract/<fileName>")
def download_extract(fileName):
    if session.get("TEMP_NAME", None) is not None:
        path1 = os.path.join(app.config["EXTRACTION_FILE_PATH"], session.get("TEMP_NAME"))
        os.remove(path1)
        session.pop("TEMP_NAME", None)
        try:
            return send_from_directory(app.config["DOWNLOAD_EXTRACT"], fileName, as_attachment=True)
        except FileNotFoundError:
            abort(404)
    else:
        return redirect(url_for('index'))

