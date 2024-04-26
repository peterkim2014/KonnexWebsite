from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.contact import Contact
import re
import requests
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

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



@app.route('/contact_form')
def contact_form_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)

    error_message = session.pop('error_message', None)

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("contactFormTablet.html", error_message=error_message)
        else:
            print("Iphone")
            return render_template("contactFormMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("contactForm.html", error_message=error_message)
    

@app.route('/join_the_team')
def join_team_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()
    device_type = detect_device(user_agent)
    
    error_message = session.pop('error_message', None)
    
    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("joinTeamTablet.html", error_message=error_message)
        else:
            print("Iphone")
            return render_template("joinTeamMobile.html", error_message=error_message)
    else:
        print("Desktop")
        return render_template("joinTeam.html", error_message=error_message)


@app.route('/contact_form', methods=["POST"])
def contact_form():
    data = {
        'name': request.form['name'],
        'subject': request.form['subject'],
        'email': request.form['email'],
        'body': request.form['body'],
    }
    

    errors = Contact.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("contact_form_page", _anchor="contact_form"))
    else:
        Contact.create(data)
        return redirect("/contact_form")


@app.route('/join_form', methods=["POST"])
def join_form():
    data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "phone_type": request.form["phone_type"],
            "phone_number": request.form["phone_number"],
            "position": request.form["position"],
            "years_of_experience": request.form["years_of_experience"],
            "reason_for_apply": request.form["reason_for_apply"],
            "website": request.form["website"],
            "github": request.form["github"],
            "behance": request.form["behance"],
            "document": request.files['document'],
            "other": request.form["other"],
            "checkbox-consent": request.form.get("checkbox-consent")
        }


    
    errors = Team.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("join_team_page", _anchor="apply_form"))
    else:
        Team.create(data)
        return redirect("/join_the_team")



@app.route('/contactUsEmail', methods=['POST'])
def mailchimp_contactUs():
    try:
        # Extract email address from the request body
        email_address = "peterkim2014@gmail.com"

        # Construct the URL for triggering the customer journey
        url = 'https://us22.api.mailchimp.com/3.0/customer-journeys/journeys/395/steps/1275/actions/trigger'

        # Set the Mailchimp API key
        api_key = 'Bearer 31156e977e144c2224ed14d96fe11889-us22'

        # Set the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key
        }

        # Construct the request body
        body = {
            'email_address': email_address
        }

        # Make the POST request to trigger the customer journey
        response = requests.post(url, headers=headers, json=body)

        # Check the response status code
        if response.status_code == 204:
            return jsonify({"message": "Customer journey triggered successfully"}), 200
        else:
            return jsonify({"error": "Failed to trigger customer journey"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/joinTeamEmail', methods=['POST'])
def mailchimp_joinTeam():
    try:
        # Extract email address from the request body
        email_address = "peterkim2014@gmail.com"

        # Construct the URL for triggering the customer journey
        url = 'https://us22.api.mailchimp.com/3.0/customer-journeys/journeys/396/steps/1277/actions/trigger'

        # Set the Mailchimp API key
        api_key = 'Bearer 31156e977e144c2224ed14d96fe11889-us22'

        # Set the headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': api_key
        }

        # Construct the request body
        body = {
            'email_address': email_address
        }

        # Make the POST request to trigger the customer journey
        response = requests.post(url, headers=headers, json=body)

        # Check the response status code
        if response.status_code == 204:
            return jsonify({"message": "Customer journey triggered successfully"}), 200
        else:
            return jsonify({"error": "Failed to trigger customer journey"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500