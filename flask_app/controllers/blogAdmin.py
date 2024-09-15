from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
import re
from flask_app.models.blogs import Blog
import os

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
    # Fetch all blogs if the feature is 'blogsList'
    blogs = []
    if feature == 'blogsList':
        blogs = Blog.get_all()
    return render_template('blogDashboard.html', feature=feature, blogs=blogs)


@app.route('/admin/blog/content', methods=['GET', 'POST'])
def save_blog():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        header = request.form['header']
        body = request.form['body']
        tags = request.form['tags']

        # Handle the thumbnail upload
        thumbnail = request.files['thumbnail']
        thumbnail_filename = None
        if thumbnail:
            # Save the uploaded thumbnail file
            thumbnail_filename = thumbnail.filename
            thumbnail.save(os.path.join('flask_app/static/uploads', thumbnail_filename))

        # Prepare data for saving to the database
        blog_data = {
            "title": title,
            "header": header,
            "body": body,
            "thumbnail": thumbnail_filename,
            "tags": tags
        }

        # Save the blog post
        Blog.save(blog_data)
        flash('Blog saved successfully', 'success')
        return redirect(url_for('save_blog'))

    return render_template('blogDashboard.html')


@app.template_filter('process_tags')
def process_tags(tags_string):
    if not tags_string:
        return []
    # Split the tags string by commas, strip extra spaces, and return a list
    return [tag.strip() for tag in tags_string.split(',')]

# Register the filter in your Flask app
app.jinja_env.filters['process_tags'] = process_tags