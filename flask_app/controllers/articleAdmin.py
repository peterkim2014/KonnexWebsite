from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
import re
from flask_app.models.articles import Article
import os
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from flask_app.config.authorized import AUTHORIZED_USERNAME, AUTHORIZED_PASSWORD
from flask_wtf.csrf import generate_csrf

csrf = CSRFProtect(app)

AUTHORIZED_USERNAME = AUTHORIZED_USERNAME
AUTHORIZED_PASSWORD = AUTHORIZED_PASSWORD


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


@app.route('/admin/article')
def articles_adminHome():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)

    error_message = session.pop('error_message', None)
    csrf_token = generate_csrf()

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            # return render_template("articleTablet.html", error_message=error_message)
        else:
            print("Iphone")
            # return render_template("articleMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("admin/articleLogin.html", error_message=error_message, csrf_token=csrf_token)
    

@app.route('/admin/article/login', methods=['POST'])
@csrf.exempt  # CSRF protection can be bypassed in the login route only, but still, POST requests are used
def articles_login():
    # Retrieve the login credentials from the form
    username = request.form['username']
    password = request.form['password']

    # Check if the provided credentials match the authorized user
    if username == AUTHORIZED_USERNAME and password == AUTHORIZED_PASSWORD:
        session['user_id'] = AUTHORIZED_USERNAME  # Store the user in session
        flash('Login successful', 'success')
        return redirect(url_for('articles_adminDashboard'))
    
    # If credentials are invalid
    flash('Invalid username or password', 'danger')
    return redirect(url_for('articles_adminHome'))

@app.route('/admin/article/dashboard')
def articles_adminDashboard():
    if 'user_id' not in session or session['user_id'] != AUTHORIZED_USERNAME:
        flash('You must log in to access the dashboard', 'danger')
        return redirect(url_for('articles_adminHome'))

    csrf_token = generate_csrf() 
    feature = request.args.get('feature', 'thumbnail')  # Default to 'thumbnail'
    # Fetch all articles if the feature is 'articlesList'
    articles = []
    if feature == 'articlesList':
        articles = Article.get_all()
    return render_template('articleDashboard.html', feature=feature, articles=articles, csrf_token=csrf_token)


@app.route('/admin/article/content', methods=['GET', 'POST'])
@csrf.exempt
def save_article():
    if request.method == 'POST':
        # Retrieve form data
        title = request.form['title']
        header = request.form['header']
        body = request.form['body']
        sources = request.form['sources']
        tags = request.form['tags']

        

        # Handle the thumbnail upload
        thumbnail = request.files['thumbnail']
        thumbnail_filename = None
        if thumbnail:
            # Save the uploaded thumbnail file
            thumbnail_filename = thumbnail.filename
            thumbnail.save(os.path.join('flask_app/static/uploads', thumbnail_filename))

        # Prepare data for saving to the database
        article_data = {
            "title": title,
            "header": header,
            "body": body,
            "thumbnail": thumbnail_filename,
            "sources": sources,
            "tags": tags
        }

        # Save the blog post
        Article.save(article_data)
        flash('Article saved successfully', 'success')
        return redirect(url_for('save_article'))

    return render_template('articleDashboard.html')


@app.template_filter('process_tags')
def process_tags(tags_string):
    if not tags_string:
        return []
    # Split the tags string by commas, strip extra spaces, and return a list
    return [tag.strip() for tag in tags_string.split(',')]

# Register the filter in your Flask app
app.jinja_env.filters['process_tags'] = process_tags