from flask import render_template, redirect, request, flash, session
from flask_app import app
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


@app.route('/about')
def about_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()

    if is_mobile(user_agent):
        return render_template("aboutMobile.html")
    else:
        return render_template("about.html")