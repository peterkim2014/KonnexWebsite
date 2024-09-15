from flask import render_template, redirect, request, flash, session
from flask_app import app
import re
from flask_app.models.blogs import Blog

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

    # Fetch all blogs from the database using the class method get_all
    blogs = Blog.get_all()

    # Detect if a blog is selected from the query parameter
    selected_blog_id = request.args.get('blog_id')

    # If a blog_id is provided, select the appropriate blog from the database
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
