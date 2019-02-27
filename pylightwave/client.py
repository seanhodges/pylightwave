
import json
import requests

URL_ROOT = 'https://publicapi.lightwaverf.com'
URL_STRUCTURE_LIST = URL_ROOT + '/v1/structures'
URL_STRUCTURE_DETAILS = URL_ROOT + '/v1/structure/%s'
URL_FEATURE_VALUE = URL_ROOT + '/v1/feature/%s'
URL_BATCH_FEATURE_VALUE = URL_ROOT + '/v1/features/%s'


class LWClient:

    def __init__(self, auth):
        self.auth = auth

    def get_structure_list(self):
        response = requests.get(URL_STRUCTURE_LIST, \
                headers=self.__build_headers())
        return json.loads(response.text)

    def get_structure_details(self, structure_id):
        response = requests.get(URL_STRUCTURE_DETAILS % structure_id, \
                headers=self.__build_headers())
        return json.loads(response.text)

    def get_feature_value(self, feature_id):
        response = requests.get(URL_FEATURE_VALUE % feature_id, \
                headers=self.__build_headers())
        return json.loads(response.text)['value']

    def set_feature_value(self, feature_id):
        body = json.dumps({ 'value': value })
        response = requests.post(URL_FEATURE_VALUE % feature_id, data=body, \
                headers=self.__build_headers())
        return response.status == 200

    def get_feature_values(self, feature_ids):
        body = json.dumps({ 'features': features_value_pairs })
        response = requests.post(URL_BATCH_FEATURE_VALUE % 'read', data=body, \
                headers=self.__build_headers())
        return json.loads(response.text)

    def set_feature_values(self, feature_value_pairs):
        body = json.dumps({ 'features': features_value_pairs })
        response = requests.post(URL_BATCH_FEATURE_VALUE % 'write', data=body, \
                headers=self.__build_headers())
        return response.status == 200

    def __build_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'bearer %s' % self.auth['access_token'],
        }

