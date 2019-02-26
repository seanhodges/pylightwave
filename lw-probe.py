"""LW command line tool

Usage:
  lw-probe.py authenticate <bearer> <refresh>
  lw-probe.py [--file=FILE] list all
  lw-probe.py (-h | --help)
  lw-probe.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --file=FILE   Write output to file

"""

import os
import json
import requests
import yaml
from docopt import docopt

URL_AUTH = 'https://auth.lightwaverf.com/token'
URL_ROOT = 'https://publicapi.lightwaverf.com'
URL_GET_STRUCTURE_LIST = URL_ROOT + '/v1/structures'
URL_GET_STRUCTURE_DETAILS = URL_ROOT + '/v1/structure/%s'
URL_GET_FEATURE_DETAILS = URL_ROOT + '/v1/feature/%s'

EXCLUDED_DEVICES = ['L2'] # Don't include the LinkPlus in the structure response (contains geolocation info)


class LWAuth:

    def authenticate(self, auth_token, refresher_token):
        headers = {
            'Authorization': 'basic %s' % auth_token,
        }
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresher_token
        }
        response = requests.post(URL_AUTH, body, headers=headers)
        return json.loads(response.text)

    def store_token(self, auth):
        print auth['access_token']
        with open('.auth.yaml', 'w') as file_handle:
            yaml.safe_dump(auth, file_handle, default_flow_style=False, encoding='utf-8', allow_unicode=True)


    def get_token(self):
        if os.path.isfile('.auth.yaml'):
            with open('.auth.yaml', 'r') as stream:
                return yaml.load(stream)
        else:
            raise 'Please authenticate before sending commands'


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

class StructureHelper:

    def __init__(self, client):
        self.client = client

    def parse_structures(self):
        result = []
        root = self.client.get_structure_list()
        for structureId in root['structures']:
            group_details = self.client.get_structure_details(structureId)
            print 'Found group: %s' % group_details['name']
            result.append({
                'name': group_details['name'],
                'devices': self.__parse_devices(group_details['devices'])
            })
        return result

    def __parse_devices(self, devices):
        result_devices = []
        for device in devices:
            if device['productCode'] not in EXCLUDED_DEVICES:
                result_devices.append({
                    'name': device['name'],
                    'productCode': device['productCode'],
                    'features': self.__parse_features(device['featureSets'])
                })
                print 'Found device: %s' % device['name']
        return result_devices


    def __parse_features(self, feature_sets):
        result_features = []
        for feature_set in feature_sets:
            for feature in feature_set['features']:
                feature_details = self.client.get_feature_details(feature['featureId'])
                result_features.append({
                    'id': feature['featureId'],
                    'type': feature['type'],
                    'writable': feature['writable'],
                    'value': feature_details['value']
                })
        return result_features


class OutputWriter:

    def print_output(self, data, to_file=False):
        if to_file:
            self.__print_to_file(data, to_file)
        else:
            self.__print_to_stdout(data)

    def __print_to_stdout(self, data):
        print yaml.safe_dump(data, encoding='utf-8', allow_unicode=True)

    def __print_to_file(self, data, output_file):
        with open(output_file, 'w') as file_handle:
            yaml.safe_dump(data, file_handle, encoding='utf-8', allow_unicode=True)
        print 'Output written to %s' % output_file


def main():
    arguments = docopt(__doc__, version='1.0')
    lwtokens = LWAuth()

    if arguments['authenticate'] and arguments['<bearer>'] and arguments['<refresh>']:
        auth = lwtokens.authenticate(arguments['<bearer>'], arguments['<refresh>'])
        lwtokens.store_token(auth)
    elif arguments['list'] and arguments['all']:
        client = LWClient(lwtokens.get_token())
        devices = StructureHelper(client).parse_structures()
        OutputWriter().print_output(devices, arguments['--file'])
    else:
        print 'Command not supported at this time'
        exit(1)



if __name__ == '__main__':
    main()
