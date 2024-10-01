from flask import render_template, redirect, request, flash, session, url_for
from flask_app import app
import re
from flask_app.models.articles import Article
import os
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash
from flask_app.config.authorized import AUTHORIZED_USERNAME, AUTHORIZED_PASSWORD
from flask_wtf.csrf import generate_csrf
import bleach
from datetime import datetime

csrf = CSRFProtect(app)

AUTHORIZED_USERNAME = AUTHORIZED_USERNAME
AUTHORIZED_PASSWORD = AUTHORIZED_PASSWORD

# Allow the tags that TinyMCE might generate
ALLOWED_TAGS = ['p', 'b', 'i', 'em', 'strong', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'br', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote', 'pre', 'code']

# Allow attributes for links, images, and headers
ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'width', 'height'],
    'p': ['style'],    # Allow inline styles (for size, alignment, etc.)
    'h1': ['style'],   # Allow inline styles for headers
    'h2': ['style'],   # Inline styles for other headers too
    'h3': ['style'],
    'h4': ['style'],
    'h5': ['style'],
    'h6': ['style'],
    'pre': ['class'],  # Allow class for code blocks
    'code': ['class'], # Allow class for inline code styling
    'table': ['border', 'style'],
    'th': ['colspan', 'rowspan'],
    'td': ['colspan', 'rowspan']
}


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
        article_id = request.args.get('article_id')  # Get article_id if available
        title = request.form['title']
        header = request.form['header']
        body = request.form['body']  # This is the raw HTML content
        sources = request.form['sources']
        tags = request.form['tags']
        created_at = request.form['createdAt']  # Get the createdAt date

        # Convert createdAt from string to datetime format (for saving in database)
        try:
            created_at = datetime.strptime(created_at, '%m-%d-%Y')
        except ValueError:
            flash('Invalid date format for Created At. Please use mm-dd-yyyy.', 'danger')
            return redirect(request.url)

        # Sanitize the body content using Bleach
        sanitized_body = bleach.clean(body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=False)

        # Handle the thumbnail upload
        thumbnail = request.files['thumbnail']
        thumbnail_filename = None
        if thumbnail:
            thumbnail_filename = thumbnail.filename
            thumbnail.save(os.path.join('flask_app/static/uploads', thumbnail_filename))

        # Prepare data for saving to the database
        article_data = {
            "title": title,
            "header": header,
            "body": sanitized_body,  # Store the sanitized content
            "thumbnail": thumbnail_filename,
            "sources": sources,
            "tags": tags,
            "created_at": created_at  # Add created_at to the data
        }

        # If article_id is provided, update the existing article
        if article_id:
            article_data['id'] = article_id
            Article.update(article_data)
            flash('Article updated successfully', 'success')
        else:
            # Save new article
            Article.save(article_data)
            flash('Article saved successfully', 'success')

        return redirect(url_for('articles_adminDashboard', feature='articlesList'))
    
    return render_template('articleDashboard.html')



@app.template_filter('process_tags')
def process_tags(tags_string):
    if not tags_string:
        return []
    # Split the tags string by commas, strip extra spaces, and return a list
    return [tag.strip() for tag in tags_string.split(',')]

# Register the filter in your Flask app
app.jinja_env.filters['process_tags'] = process_tags


@app.route('/admin/article/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    if 'user_id' not in session or session['user_id'] != AUTHORIZED_USERNAME:
        flash('You must be logged in to delete articles', 'danger')
        return redirect(url_for('articles_adminHome'))
    
    # Fetch the article by ID and delete it
    article = Article.get_by_id(article_id)
    if article:
        Article.delete(article_id)
        flash('Article deleted successfully', 'success')
    else:
        flash('Article not found', 'danger')

    return redirect(url_for('articles_adminDashboard', feature='articlesList'))

@app.route('/admin/article/edit/<int:article_id>', methods=['GET'])
def edit_article(article_id):
    if 'user_id' not in session or session['user_id'] != AUTHORIZED_USERNAME:
        flash('You must be logged in to edit articles', 'danger')
        return redirect(url_for('articles_adminHome'))

    # Fetch the article by ID
    article = Article.get_by_id(article_id)
    if article:
        csrf_token = generate_csrf()  # Generate a CSRF token for the form
        return render_template('admin/articleContent.html', article=article, csrf_token=csrf_token)
    else:
        flash('Article not found', 'danger')
        return redirect(url_for('articles_adminDashboard', feature='articlesList'))
