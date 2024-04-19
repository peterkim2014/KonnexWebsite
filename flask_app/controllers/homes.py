from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
import re
from flask_app.models.waitlist import Waitlist


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




@app.route('/')
def landing_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()

    if is_mobile(user_agent):
        error_message = session.pop('error_message', None)
        return render_template("homepageMobile.html", error_message=error_message)
    else:
        error_message = session.pop('error_message', None)
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