from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
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


@app.route('/admin/blog')
def blogs_adminHome():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)

    error_message = session.pop('error_message', None)

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            # return render_template("blogTablet.html", error_message=error_message)
        else:
            print("Iphone")
            # return render_template("blogMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("admin/blogLogin.html", error_message=error_message)
    

@app.route('/admin/blog/login', methods=['POST'])
def blogs_login():
    # Perform login logic
    # If successful, redirect to dashboard
    # Assuming login is successful here for demonstration purposes
    return redirect(url_for('blogs_adminDashboard'))

@app.route('/admin/blog/dashboard')
def blogs_adminDashboard():
    feature = request.args.get('feature', 'thumbnail')  # Default to 'thumbnail'
    return render_template('blogDashboard.html', feature=feature)