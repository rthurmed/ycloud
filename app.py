import os
from pathlib import Path

from flask import Flask, request, render_template, redirect, abort, send_file

from service.counter import counter_service
from service.file import file_service, FileAlreadyExistsException

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/counter")
def counter():
    counter_service.increment()
    return render_template("fragment/counter.html", count=counter_service.get_value())

@app.get("/file")
def get_all_file():
    files = file_service.get_all()
    return render_template("fragment/files.html", files=files)

@app.get("/file/<name>")
def get_file(name: str):
    file = file_service.get(name)
    return send_file(file.path, as_attachment=True)

@app.post("/file")
def post_file():
    if "file" not in request.files:
        abort(400)
    
    file = request.files["file"]

    try:
        file_service.store(file)
    except FileAlreadyExistsException as exc:
        abort(400)

    files = file_service.get_all()
    return render_template("fragment/files.html", files=files)
    
