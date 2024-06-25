from flask import render_template, redirect, request, flash, session, url_for, jsonify
from flask_app import app
from flask_app.models.team import Team
from flask_app.models.contact import Contact
import re
import requests
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from flask_app.config.mailMarketing import API_KEY

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
    headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "content-type": "application/json",
        "Authorization": API_KEY
    }
    update_headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "Authorization": API_KEY
    }


    
    createProfileURL = 'https://a.klaviyo.com/api/profiles/'
    addProfileToWaitlist = 'https://a.klaviyo.com/api/lists/X3vCzT/relationships/profiles/'
    addProfileToContact = 'https://a.klaviyo.com/api/lists/VtXY46/relationships/profiles/'

    name = data["name"]
    new_format = name.split(" ")
    first_name = new_format[0]
    last_name = new_format[1]

    email = data["email"]
    new_email_format = email.split("@")
    email_name = new_email_format[0]
    email_domain = new_email_format[1]
    print(email, new_email_format)

    findProfile_url = f'https://a.klaviyo.com/api/profiles/?fields[profile]=email&page[size]=20'
    # print(findProfile_url)

    response = requests.get(findProfile_url, headers=update_headers)
    # print(response.text)
    existingAccdata = []
    existingAccdata.append(response.json())
    print("This is data: ", existingAccdata[0]["data"])
    accountsFormattedData = existingAccdata[0]["data"]

        # Assuming 'data' is defined and contains the email you want to match
    print("Email to match: ", data["email"])

    email_found = False
    account_id = None
    for account in accountsFormattedData:
        print("Checking account: ", account["attributes"]["email"])  # Debugging line
        if account["attributes"]["email"] == data["email"]:
            print("Exists")
            payload = { "data": {
            "type": "profile",
            "id": account["id"],
            "meta": { "patch_properties": {
                    "append": { 
                        "subject": data["subject"],
                        "body": data["body"] 
                    },
                } 
            }
        }}
            update_url = f'https://a.klaviyo.com/api/profiles/{account["id"]}/'
            response = requests.patch(update_url, json=payload, headers=headers)
            print("Response : ", response)

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": account["id"]
                    }
                ] 
            }
            print("Data input: ", addProfileToTeam_data)
            addProfileToTeamResponse = requests.post(addProfileToContact, json=addProfileToTeam_data, headers=headers)
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
                    "first_name": first_name,
                    "last_name": last_name,
                    "properties": {
                        "subject": data["subject"],
                        "body": data["body"] 
                    }
                }
            }
        }

        createProfileResponse = requests.post(createProfileURL, json=profile_data, headers=headers)
        print("Create profile response: ", createProfileResponse.json())
        
        user_data_temp = createProfileResponse.json()
        print("User temp data: ", user_data_temp)

        if "errors" in user_data_temp:
            print("Duplicate profile found")
            duplicate_profile_id = user_data_temp["errors"][0]["meta"]["duplicate_profile_id"]
            print("Duplicate profile ID: ", duplicate_profile_id)
            
            payload = { "data": {
            "type": "profile",
            "id": account["id"],
            "meta": { "patch_properties": {
                    "append": { 
                        "subject": data["subject"],
                        "body": data["body"] 
                    },
                } 
            }}}
            update_url = f'https://a.klaviyo.com/api/profiles/{duplicate_profile_id}/'
            response = requests.patch(update_url, json=payload, headers=headers)
            print("Response : ", response)

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": duplicate_profile_id
                    }
                ] 
            }
            print("Data input: ", addProfileToTeam_data)
            addProfileToTeamResponse = requests.post(addProfileToContact, json=addProfileToTeam_data, headers=headers)
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
            addProfileToTeamResponse = requests.post(addProfileToContact, json=addProfileToTeam_data, headers=headers)
            print("Add profile to Team: ", addProfileToTeamResponse)
        user_data_temp.clear()



    

    errors = Contact.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("contact_form_page", _anchor="contact_form"))
    else:
        data["marketingID"] = account_id
        if not Contact.get_by_email(data["email"]):
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
    

    headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "content-type": "application/json",
        "Authorization": API_KEY
    }
    update_headers = {
        "accept": "application/json",
        "revision": "2024-06-15",
        "Authorization": API_KEY
    }


    
    createProfileURL = 'https://a.klaviyo.com/api/profiles/'
    addProfileToTeam = 'https://a.klaviyo.com/api/lists/RphBSD/relationships/profiles/'


    phone_number = data["phone_number"]
    phone_number_format = phone_number.replace(" ","")


    findProfile_url = f'https://a.klaviyo.com/api/profiles/?fields[profile]=email&page[size]=20'
    # print(findProfile_url)

    response = requests.get(findProfile_url, headers=update_headers)
    # print(response.text)
    existingAccdata = []
    existingAccdata.append(response.json())
    print("This is data: ", existingAccdata[0]["data"])
    accountsFormattedData = existingAccdata[0]["data"]

    # Assuming 'data' is defined and contains the email you want to match
    print("Email to match: ", data["email"])

    email_found = False
    account_id = None
    for account in accountsFormattedData:
        print("Checking account: ", account["attributes"]["email"])  # Debugging line
        if account["attributes"]["email"] == data["email"]:
            print("Exists")
            payload = { 
                "data": {
                    "type": "profile",
                    "id": account["id"],
                    "phone_number": "+1" + phone_number_format,
                    "title": data["position"],
                    "meta": { 
                        "patch_properties": {
                            "append": { 
                                "years_of_experience": data["years_of_experience"],
                                "reason_for_apply": data["reason_for_apply"],
                                "website": data["website"],
                                "github": data["github"],
                                "behance": data["behance"],
                                "other": data["other"]
                            }
                        } 
                    }
                }
            }
            update_url = f'https://a.klaviyo.com/api/profiles/{account["id"]}/'
            response = requests.patch(update_url, json=payload, headers=headers)
            print("Response : ", response)

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": account["id"]
                    }
                ] 
            }
            print("Data input: ", addProfileToTeam_data)
            addProfileToTeamResponse = requests.post(addProfileToTeam, json=addProfileToTeam_data, headers=headers)
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
                    "last_name": data["last_name"],
                    "phone_number": "+1" + phone_number_format,
                    "title": data["position"],
                    "properties": {
                        "years_of_experience": data["years_of_experience"],
                        "reason_for_apply": data["reason_for_apply"],
                        "website": data["website"],
                        "github": data["github"],
                        "behance": data["behance"],
                        "other": data["other"]
                    }
                }
            }
        }

        createProfileResponse = requests.post(createProfileURL, json=profile_data, headers=headers)
        print("Create profile response: ", createProfileResponse.json())
        
        user_data_temp = createProfileResponse.json()
        print("User temp data: ", user_data_temp)

        if "errors" in user_data_temp:
            print("Duplicate profile found")
            duplicate_profile_id = user_data_temp["errors"][0]["meta"]["duplicate_profile_id"]
            print("Duplicate profile ID: ", duplicate_profile_id)
            
            payload = { 
                "data": {
                    "type": "profile",
                    "id": duplicate_profile_id,
                    "phone_number": "+1" + phone_number_format,
                    "title": data["position"],
                    "meta": { 
                        "patch_properties": {
                            "append": { 
                                "years_of_experience": data["years_of_experience"],
                                "reason_for_apply": data["reason_for_apply"],
                                "website": data["website"],
                                "github": data["github"],
                                "behance": data["behance"],
                                "other": data["other"]
                            }
                        } 
                    }
                }
            }
            update_url = f'https://a.klaviyo.com/api/profiles/{duplicate_profile_id}/'
            response = requests.patch(update_url, json=payload, headers=headers)
            print("Response : ", response)

            addProfileToTeam_data = { 
                "data": [
                    {
                        "type": "profile",
                        "id": duplicate_profile_id
                    }
                ] 
            }
            print("Data input: ", addProfileToTeam_data)
            addProfileToTeamResponse = requests.post(addProfileToTeam, json=addProfileToTeam_data, headers=headers)
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
            addProfileToTeamResponse = requests.post(addProfileToTeam, json=addProfileToTeam_data, headers=headers)
            print("Add profile to Team: ", addProfileToTeamResponse)
        user_data_temp.clear()






    
    errors = Team.validate_inputs(data)
    if errors:
        # If there are errors, store them in the session and redirect
        session['error_message'] = errors
        return redirect(url_for("join_team_page", _anchor="apply_form"))
    else:
        data["marketingID"] = account_id
        if not Team.get_by_email(data["email"]):
            Team.create(data)
        return redirect("/join_the_team")



