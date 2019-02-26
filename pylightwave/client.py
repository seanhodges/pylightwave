
import json
import requests

URL_ROOT = 'https://publicapi.lightwaverf.com'
URL_GET_STRUCTURE_LIST = URL_ROOT + '/v1/structures'
URL_GET_STRUCTURE_DETAILS = URL_ROOT + '/v1/structure/%s'
URL_GET_FEATURE_DETAILS = URL_ROOT + '/v1/feature/%s'


class LWClient:

    def __init__(self, auth):
        self.auth = auth

    def get_structure_list(self):
        response = requests.get(URL_GET_STRUCTURE_LIST, headers=self.__build_headers())
        return json.loads(response.text)

    def get_structure_details(self, structureId):
        response = requests.get(URL_GET_STRUCTURE_DETAILS % structureId, headers=self.__build_headers())
        return json.loads(response.text)

    def get_feature_details(self, featureId):
        response = requests.get(URL_GET_FEATURE_DETAILS % featureId, headers=self.__build_headers())
        return json.loads(response.text)

    def __build_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'bearer %s' % self.auth['access_token'],
        }

