from flask import render_template, redirect, request, flash, session
from flask_app import app


@app.route('/')
def landing_page():
    return render_template("homepage.html")