from flask import render_template, redirect, request, flash, session
from flask_app import app
import re
from flask_app.models.articles import Article
from bs4 import BeautifulSoup

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


def strip_headers_only_paragraphs(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Remove all header tags (h1 to h6)
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        header.decompose()

    # Return only the paragraph content
    paragraphs = soup.find_all('p')
    return ''.join(str(p) for p in paragraphs)


@app.route('/articles')
def articles_home():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)
    error_message = session.pop('error_message', None)

    previewText = ""

    # Fetch all articles from the database using the class method get_all
    articles = Article.get_all()
    for article in articles:
        if isinstance(article['thumbnail'], bytes):
            article['thumbnail'] = article['thumbnail'].decode('utf-8')  # Decode from bytes to string
        print(f"Thumbnail: {article['thumbnail']}")

        # Process the article body to strip headers and keep only paragraphs
        previewText = strip_headers_only_paragraphs(article['body'])
        article['previewText'] = strip_headers_only_paragraphs(article['body'])[:200]  # Only keep the first 200 characters
        print(f"Processed Article Body: {previewText}")

    # # Detect if a article is selected from the query parameter
    selected_article_id = request.args.get('article_id')

    # # If a article_id is provided, select the appropriate article from the database
    selected_article = None
    if selected_article_id:
        selected_article = next((article for article in articles if article['id'] == int(selected_article_id)), None)


    # Return the appropriate template based on device type
    if device_type:
        if "ipad" in user_agent:
            print("iPad detected")
            return render_template("articleTablet.html", selected_article=selected_article, articles=articles, error_message=error_message, previewText=previewText)
        else:
            print("Mobile device detected")
            return render_template("articleMobile.html", selected_article=selected_article, articles=articles, error_message=error_message, previewText=previewText)
    else:
        print("Desktop detected")
        return render_template("article.html", selected_article=selected_article, articles=articles, error_message=error_message, previewText=previewText)
