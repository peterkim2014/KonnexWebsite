from flask import render_template, redirect, request, flash, session
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.contact import Contact
import re

def is_mobile(user_agent):
    # Regular expressions for common mobile device strings
    mobile_patterns = [
        "iphone", "ipod", "ipad", "android", "blackberry",
        "windows phone", "nokia", "samsung", "mobile"
    ]
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent):
            print(f"Detected mobile device: {user_agent}")
            return True
    print(f"Not a mobile device: {user_agent}")
    return False



@app.route('/contact_form')
def contact_form_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()

    if is_mobile(user_agent):
        return render_template("contactFormMobile.html")
    else:
        return render_template("contactForm.html")
    

@app.route('/join_the_team')
def join_team_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()

    if is_mobile(user_agent):
        return render_template('joinTeamMobile.html')
    else:
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
            "document": request.files['document'],
            "other": request.form["other"],
        }
    Team.create(data)

    return redirect("/join_the_team")
