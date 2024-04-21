from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.contact import Contact
import re

def detect_device(user_agent):
    # Regular expressions for common mobile and tablet device strings
    mobile_patterns = [
        "iphone", "ipod", "ipad", "android", "blackberry",
        "windows phone", "nokia", "samsung", "mobile", "tablet"
    ]
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent, re.IGNORECASE):
            print(f"Detected mobile or tablet device: {user_agent}")
            return True
    print(f"Not a mobile or tablet device: {user_agent}")
    return False



@app.route('/contact_form')
def contact_form_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)

    error_message = session.pop('error_message', None)

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("contactFormTablet.html", error_message=error_message)
        else:
            print("Iphone")
            return render_template("contactFormMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("contactForm.html", error_message=error_message)
    

@app.route('/join_the_team')
def join_team_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)
    
    error_message = session.pop('error_message', None)
    
    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("joinTeamTablet.html", error_message=error_message)
        else:
            print("Iphone")
            return render_template("joinTeamMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("joinTeam.html", error_message=error_message)


@app.route('/contact_form', methods=["POST"])
def contact_form():
    data = {
        'name': request.form['name'],
        'subject': request.form['subject'],
        'email': request.form['email'],
        'body': request.form['body'],
    }
    

    errors = Contact.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("contact_form_page", _anchor="contact_form"))
    else:
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


    
    errors = Team.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("join_team_page", _anchor="apply_form"))
    else:
        Team.create(data)
        return redirect("/join_the_team")
