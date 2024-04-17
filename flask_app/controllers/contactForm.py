from flask import render_template, redirect, request, flash, session
from flask_app import app

@app.route('/contact-form')
def contact_form_page():
    return render_template("contactForm.html")