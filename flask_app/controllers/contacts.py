from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.contact import Contact

@app.route('/contact_form')
def contact_form_page():
    return render_template("contactForm.html")

@app.route('/join_the_team')
def join_team_page():
    return render_template("joinTeam.html")


@app.route('/contact_form', methods=["POST"])
def contact_form():
    data = {
        'name': request.form['name'],
        'subject': request.form['subject'],
        'email': request.form['email'],
        'body': request.form['body'],
    }
    Contact.create(data)
    return redirect("/contact_form")


@app.route('/join_form', methods=["POST"])
def join_form():
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "phone_type": request.form["phone_type"],
            "phone_number": request.form["phone_number"],
            "position": request.form["position"],
            "years_of_experience": request.form["years_of_experience"],
            "reason_for_apply": request.form["reason_for_apply"],
            "website": request.form["website"],
            "github": request.form["github"],
            "behance": request.form["behance"],
            "other": request.form["other"],
        }
    Team.create(data)

    return redirect("/join_the_team")
