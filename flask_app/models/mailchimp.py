import requests,json
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from flask_app.config.mailMarketing import MAILCHIMP_API_KEY, MAILCHIMP_SERVER_PREFIX

class Mailchimp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = f'https://us22.api.mailchimp.com/3.0/'

    def test_function(self):

        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": MAILCHIMP_API_KEY,
            "server": MAILCHIMP_SERVER_PREFIX
        })
        response = client.customerJourneys.trigger(1100, 3888, {"email_address": "pkim@konnexwallet.io"})
        return response
    
    @classmethod
    def add_member_to_list(cls, data, header):
        url = 'https://us22.api.mailchimp.com/3.0/lists/43b63d0cce/members'

        auth = ('pkim_konnex', MAILCHIMP_API_KEY)
        # Set the headers
        # response = requests.post(url, auth=auth, json=data, headers=header)
        response = requests.post(url, auth=auth, json=data)
        print(response)
        # return response.json()
