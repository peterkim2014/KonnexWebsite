from flask import render_template, redirect, request, flash, session, url_for, send_from_directory
from flask_app import app
import re
import os
from flask_app.models.waitlist import Waitlist

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))


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




@app.route('/')
def landing_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()    
    device_type = detect_device(user_agent)

    error_message = session.pop('error_message', None)

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("homepageTablet.html", error_message=error_message)
        else:
            print("Iphone")
            return render_template("homepageMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("homepage.html", error_message=error_message)

    

@app.route('/waitlist_form', methods=["POST"])
def waitlist_form():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"]
    }

    errors = Waitlist.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("landing_page", _anchor="join_waitlist"))
    else:
        Waitlist.create(data)
        return redirect("/")
    

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)