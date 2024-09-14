from flask import render_template, redirect, request, flash, session
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


@app.route('/blogs')
def blogs_home():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)
    error_message = session.pop('error_message', None)

    # Detect if a blog is selected from the query parameter
    selected_blog_id = request.args.get('blog_id')

    # Sample blog data for demonstration purposes
    blogs = [
        {'id': 1, 'title': 'Introduction to Konnex', 'content': 'Welcome to the Konnex Blog!'},
        {'id': 2, 'title': 'The Future of Cryptocurrency', 'content': 'What does the future hold for crypto?'},
        {'id': 3, 'title': 'Blockchain Basics', 'content': 'Understanding the basics of blockchain.'}
    ]

    # If a blog_id is provided, select the appropriate blog
    selected_blog = None
    if selected_blog_id:
        selected_blog = next((blog for blog in blogs if blog['id'] == int(selected_blog_id)), None)

    # Return the appropriate template based on device type
    if device_type:
        if "ipad" in user_agent:
            print("iPad detected")
            return render_template("blogTablet.html", selected_blog=selected_blog, blogs=blogs, error_message=error_message)
        else:
            print("Mobile device detected")
            return render_template("blogMobile.html", selected_blog=selected_blog, blogs=blogs, error_message=error_message)
    else:
        print("Desktop detected")
        return render_template("blog.html", selected_blog=selected_blog, blogs=blogs, error_message=error_message)
