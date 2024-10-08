from flask import render_template, redirect, request, flash, session, url_for, send_from_directory, jsonify
from flask_app import app
import re
import os
from flask_app.models.waitlist import Waitlist
from flask_app.models.email import Email
import requests
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import generate_csrf


STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

csrf = CSRFProtect(app)


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

@app.route('/screen-size', methods=['POST'])
def screen_size():
    screen_data = request.get_json()
    width = screen_data.get('width')
    height = screen_data.get('height')
    
    if width == 1440 and height == 900:
        print("13-inch MacBook Air")
    elif width == 1680 and height == 1050:
        print("15-inch MacBook Air")
    return '', 204


@app.route('/')
def landing_page():
    user_agent = request.headers.get('User-Agent')
    user_agent = user_agent.lower()    
    device_type = detect_device(user_agent)
    csrf_token = generate_csrf()
    error_message = session.pop('error_message', None)

    if device_type == True:
        if "ipad" in user_agent:
            print("Ipad")
            return render_template("homepageTablet.html", error_message=error_message, csrf_token=csrf_token)
        else:
            print("Iphone")
            return render_template("homepageMobile.html", error_message=error_message, csrf_token=csrf_token)
    else:
        print("Desktop")
        return render_template("homepage.html", error_message=error_message, csrf_token=csrf_token)



@app.route('/waitlist_form', methods=["POST"])
def waitlist_form():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        'confirmed': 0
    }
    headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "content-type": "application/json",
        "Authorization": 'Klaviyo-API-Key pk_3daf1e10664e62b49b74976c4e4a22fa56'
    }
    update_headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "Authorization": 'Klaviyo-API-Key pk_3daf1e10664e62b49b74976c4e4a22fa56'
    }
    createProfileURL = 'https://a.klaviyo.com/api/profiles/'
    addProfileToWaitlist = 'https://a.klaviyo.com/api/lists/X3vCzT/relationships/profiles/'

    findProfile_url = f'https://a.klaviyo.com/api/profiles/?fields[profile]=email&page[size]=20'

    response = requests.get(findProfile_url, headers=update_headers)
    
    # Handling response from the API
    existingAccdata = []
    try:
        response_json = response.json()
        if "data" in response_json:  # Check if 'data' key exists in response
            existingAccdata.append(response_json)
            accountsFormattedData = existingAccdata[0]["data"]
            # print("This is data: ", accountsFormattedData)
        else:
            print("No 'data' key found in the response.")
            accountsFormattedData = []
    except ValueError:
        print("Error parsing JSON response.")
        accountsFormattedData = []

    # Assuming 'data' is defined and contains the email you want to match
    print("Email to match: ", data["email"])

    email_found = False
    account_id = None

    # Get the reCAPTCHA response token
    recaptcha_response = request.form['g-recaptcha-response']
    
    # Secret key from reCAPTCHA registration
    secret_key = "6LfRykAqAAAAAOEaNGdX6HrUQ7g_CUkd-oqwt4jB"

    # Verify the response with Google
    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post(verification_url, data=payload)
    result = response.json()

    if accountsFormattedData:  # Proceed only if accountsFormattedData is not empty
        for account in accountsFormattedData:
            print("Checking account: ", account["attributes"]["email"])  # Debugging line
            if account["attributes"]["email"] == data["email"]:
                print("Exists")
                addProfileToTeam_data = { 
                    "data": [
                        {
                            "type": "profile",
                            "id": account["id"]
                        }
                    ] 
                }
                print("Data input: ", addProfileToTeam_data)
                addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
                print("Add profile to Team: ", addProfileToTeamResponse)
                email_found = True
                account_id = account["id"]
                break

    if not email_found:
        profile_data = {   
            "data": {
                "type": "profile",
                "attributes": {
                    "email": data["email"],
                    "first_name": data["first_name"],
                    "last_name": data["last_name"]
                }    
            } 
        }

        createProfileResponse = requests.post(createProfileURL, json=profile_data, headers=headers)
        print("Create profile response: ", createProfileResponse.json())
        
        user_data_temp = createProfileResponse.json()
        print("User temp data: ", user_data_temp)

        if "errors" in user_data_temp:
            print("Duplicate profile found")
            duplicate_profile_id = user_data_temp["errors"][0]['meta']["duplicate_profile_id"]
            print("Duplicate profile ID: ", duplicate_profile_id)
            

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": duplicate_profile_id
                    }
                ] 
            }
            print("Data input: ", addProfileToTeam_data)
            addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
            print("Add profile to Team: ", addProfileToTeamResponse)
        else:
            user_id = user_data_temp["data"]["id"]

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": user_id
                    }
                ] 
            }
            addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
            print("Add profile to Team: ", addProfileToTeamResponse)
        user_data_temp.clear()

    # Validation and error handling
    errors = Waitlist.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("landing_page", _anchor="join_waitlist"))
    else:
        print("account_id", account_id)
        data["marketingID"] = account_id
        if not Waitlist.get_by_email(data["email"]):
            Waitlist.create(data)
        session['error_message'] = 'Confirmation email has been sent!'
        return redirect(url_for("landing_page", _anchor="join_waitlist"))

    

# @app.route('/waitlist_form', methods=["POST"])
# def waitlist_form():
#     data = {
#         "first_name": request.form["first_name"],
#         "last_name": request.form["last_name"],
#         "email": request.form["email"],
#         'confirmed': 0
#     }
#     headers = {
#         "accept": "application/json",
#         "revision": "2024-06-15",
#         "content-type": "application/json",
#         # "Authorization": API_KEY
#     }
#     update_headers = {
#         "accept": "application/json",
#         "revision": "2024-06-15",
#         # "Authorization": API_KEY
#     }
#     createProfileURL = 'https://a.klaviyo.com/api/profiles/'
#     addProfileToWaitlist = 'https://a.klaviyo.com/api/lists/X3vCzT/relationships/profiles/'

#     findProfile_url = f'https://a.klaviyo.com/api/profiles/?fields[profile]=email&page[size]=20'
#     # print(findProfile_url)

#     response = requests.get(findProfile_url, headers=update_headers)
#     # print(response.text)
#     existingAccdata = []
#     existingAccdata.append(response.json())
#     if existingAccdata != None:
#         print("This is data: ", existingAccdata[0]["data"])
#         accountsFormattedData = existingAccdata[0]["data"]

#         # Assuming 'data' is defined and contains the email you want to match
#     print("Email to match: ", data["email"])

#     email_found = False
#     account_id = None
#     # Get the reCAPTCHA response token
#     # recaptcha_response = request.form['g-recaptcha-response']
    
#     # Secret key from reCAPTCHA registration
#     # secret_key = "6LfRykAqAAAAAOEaNGdX6HrUQ7g_CUkd-oqwt4jB"

#     # Verify the response with Google
#     # verification_url = "https://www.google.com/recaptcha/api/siteverify"
#     # payload = {
#     #     'secret': secret_key,
#     #     'response': recaptcha_response
#     # }
#     # response = requests.post(verification_url, data=payload)
#     # result = response.json()

#     if accountsFormattedData:
#         for account in accountsFormattedData:
#             print("Checking account: ", account["attributes"]["email"])  # Debugging line
#             if account["attributes"]["email"] == data["email"]:
#                 print("Exists")
#                 addProfileToTeam_data = { 
#                     "data": [
#                         {
#                             "type": "profile",
#                             "id": account["id"]
#                         }
#                     ] 
#                 }
#                 print("Data input: ", addProfileToTeam_data)
#                 addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
#                 print("Add profile to Team: ", addProfileToTeamResponse)
#                 email_found = True
#                 account_id = account["id"]
#                 break

#     if not email_found:
#         profile_data = {   
#             "data": {
#                 "type": "profile",
#                 "attributes": {
#                     "email": data["email"],
#                     "first_name": data["first_name"],
#                     "last_name": data["last_name"]
#                 }    
#             } 
#         }

#         createProfileResponse = requests.post(createProfileURL, json=profile_data, headers=headers)
#         print("Create profile response: ", createProfileResponse.json())
        
#         user_data_temp = createProfileResponse.json()
#         print("User temp data: ", user_data_temp)

#         if "errors" in user_data_temp:
#             print("Duplicate profile found")
#             duplicate_profile_id = user_data_temp["errors"][0]["meta"]["duplicate_profile_id"]
#             print("Duplicate profile ID: ", duplicate_profile_id)
            

#             addProfileToTeam_data = { 
#                 "data": [
#                     {
#                         "type": "profile",
#                         "id": duplicate_profile_id
#                     }
#                 ] 
#             }
#             print("Data input: ", addProfileToTeam_data)
#             addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
#             print("Add profile to Team: ", addProfileToTeamResponse)
#         else:
#             user_id = user_data_temp["data"]["id"]

#             addProfileToTeam_data = { 
#                 "data": [
#                     {
#                         "type": "profile",
#                         "id": user_id
#                     }
#                 ] 
#             }
#             addProfileToTeamResponse = requests.post(addProfileToWaitlist, json=addProfileToTeam_data, headers=headers)
#             print("Add profile to Team: ", addProfileToTeamResponse)
#         user_data_temp.clear()







    # errors = Waitlist.validate_inputs(data)
    # if errors:
    #     # If there are errors, store them in the session and redirect
    #     session['error_message'] = errors
    #     return redirect(url_for("landing_page", _anchor="join_waitlist"))
    # else:
    #     # MAKE SURE TO TURN THIS ON 
    #     print("account_id", account_id)
    #     data["marketingID"] = account_id
    #     if not Waitlist.get_by_email(data["email"]):
    #         Waitlist.create(data)
    #     session['error_message'] = 'Confirmation email has been sent!'
    #     return redirect(url_for("landing_page", _anchor="join_waitlist"))
    

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


