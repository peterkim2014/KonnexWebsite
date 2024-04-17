from flask import render_template, redirect, request, flash, session
from flask_app import app

@app.route('/contact_form')
def contact_form_page():
    return render_template("contactForm.html")

@app.route('/join_the_team')
def join_team_page():
    return render_template("joinTeam.html")