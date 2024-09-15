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


    blogs = [
        {
            'id': 1,
            'title': 'Introduction to Konnex',
            'header': 'Getting Started with Konnex',
            'body': 'Konnex is a revolutionary cryptocurrency wallet designed for secure and easy transactions.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Wallet, Blockchain',
            'createdAt': '2024-09-10 12:30:00',
        },
        {
            'id': 2,
            'title': 'The Future of Cryptocurrency',
            'header': 'What the Future Holds for Crypto',
            'body': 'The cryptocurrency market is rapidly evolving, and Konnex is at the forefront of the change.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Future, Investment',
            'createdAt': '2024-09-12 08:45:00',
        },
        {
            'id': 3,
            'title': 'Blockchain Basics',
            'header': 'Understanding Blockchain Technology',
            'body': 'Blockchain is the backbone of all cryptocurrency transactions, and Konnex leverages it to provide security.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Blockchain, Technology, Crypto',
            'createdAt': '2024-09-13 14:00:00',
        },
        {
            'id': 4,
            'title': 'Security and Privacy in Cryptocurrency',
            'header': 'Ensuring Your Digital Assets are Secure',
            'body': 'With Konnex, security is our top priority. We use advanced encryption to protect your data and assets.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Security, Privacy, Cryptocurrency',
            'createdAt': '2024-09-14 16:20:00',
        },
        {
            'id': 5,
            'title': 'Introduction to Konnex',
            'header': 'Getting Started with Konnex',
            'body': 'Konnex is a revolutionary cryptocurrency wallet designed for secure and easy transactions.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Wallet, Blockchain',
            'createdAt': '2024-09-10 12:30:00',
        },
        {
            'id': 6,
            'title': 'The Future of Cryptocurrency',
            'header': 'What the Future Holds for Crypto',
            'body': 'The cryptocurrency market is rapidly evolving, and Konnex is at the forefront of the change.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Future, Investment',
            'createdAt': '2024-09-12 08:45:00',
        },
        {
            'id': 7,
            'title': 'Blockchain Basics',
            'header': 'Understanding Blockchain Technology',
            'body': 'Blockchain is the backbone of all cryptocurrency transactions, and Konnex leverages it to provide security.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Blockchain, Technology, Crypto',
            'createdAt': '2024-09-13 14:00:00',
        },
        {
            'id': 8,
            'title': 'Security and Privacy in Cryptocurrency',
            'header': 'Ensuring Your Digital Assets are Secure',
            'body': 'With Konnex, security is our top priority. We use advanced encryption to protect your data and assets.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Security, Privacy, Cryptocurrency',
            'createdAt': '2024-09-14 16:20:00',
        },
        {
            'id': 9,
            'title': 'Introduction to Konnex',
            'header': 'Getting Started with Konnex',
            'body': 'Konnex is a revolutionary cryptocurrency wallet designed for secure and easy transactions.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Wallet, Blockchain',
            'createdAt': '2024-09-10 12:30:00',
        },
        {
            'id': 10,
            'title': 'The Future of Cryptocurrency',
            'header': 'What the Future Holds for Crypto',
            'body': 'The cryptocurrency market is rapidly evolving, and Konnex is at the forefront of the change.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Future, Investment',
            'createdAt': '2024-09-12 08:45:00',
        },
        {
            'id': 11,
            'title': 'Blockchain Basics',
            'header': 'Understanding Blockchain Technology',
            'body': 'Blockchain is the backbone of all cryptocurrency transactions, and Konnex leverages it to provide security.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Blockchain, Technology, Crypto',
            'createdAt': '2024-09-13 14:00:00',
        },
        {
            'id': 12,
            'title': 'Security and Privacy in Cryptocurrency',
            'header': 'Ensuring Your Digital Assets are Secure',
            'body': 'With Konnex, security is our top priority. We use advanced encryption to protect your data and assets.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Security, Privacy, Cryptocurrency',
            'createdAt': '2024-09-14 16:20:00',
        },
        {
            'id': 13,
            'title': 'Introduction to Konnex',
            'header': 'Getting Started with Konnex',
            'body': 'Konnex is a revolutionary cryptocurrency wallet designed for secure and easy transactions.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Wallet, Blockchain',
            'createdAt': '2024-09-10 12:30:00',
        },
        {
            'id': 14,
            'title': 'The Future of Cryptocurrency',
            'header': 'What the Future Holds for Crypto',
            'body': 'The cryptocurrency market is rapidly evolving, and Konnex is at the forefront of the change.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Cryptocurrency, Future, Investment',
            'createdAt': '2024-09-12 08:45:00',
        },
        {
            'id': 15,
            'title': 'Blockchain Basics',
            'header': 'Understanding Blockchain Technology',
            'body': 'Blockchain is the backbone of all cryptocurrency transactions, and Konnex leverages it to provide security.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Blockchain, Technology, Crypto',
            'createdAt': '2024-09-13 14:00:00',
        },
        {
            'id': 16,
            'title': 'Security and Privacy in Cryptocurrency',
            'header': 'Ensuring Your Digital Assets are Secure',
            'body': 'With Konnex, security is our top priority. We use advanced encryption to protect your data and assets.',
            'thumbnail': 'Auto Gallery Automotive Contact Card.jpg',
            'tags': 'Security, Privacy, Cryptocurrency',
            'createdAt': '2024-09-14 16:20:00',
        }
    ]



    # Fetch all blogs from the database using the class method get_all
    # blogs = Blog.get_all()
    # for blog in blogs:
    #     if isinstance(blog['thumbnail'], bytes):
    #         blog['thumbnail'] = blog['thumbnail'].decode('utf-8')  # Decode from bytes to string
    #     print(f"Thumbnail: {blog['thumbnail']}")

    # # Detect if a blog is selected from the query parameter
    selected_blog_id = request.args.get('blog_id')

    # # If a blog_id is provided, select the appropriate blog from the database
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
