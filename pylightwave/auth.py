
import json
import requests

URL_AUTH = 'https://auth.lightwaverf.com/token'


class LWAuth:

    def refresh(self, auth_token, refresher_token):
        headers = {
            'Authorization': 'basic %s' % auth_token,
        }
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresher_token
        }
        response = requests.post(URL_AUTH, body, headers=headers)
        return json.loads(response.text)

