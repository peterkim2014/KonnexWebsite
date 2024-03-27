from flask import render_template, redirect, request, flash, session
from flask_app import app


@app.route('/about')
def about_page():
    return render_template("about.html")