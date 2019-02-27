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
import yaml
from docopt import docopt

from pylightwave.auth import LWAuth
from pylightwave.client import LWClient


EXCLUDED_DEVICES = ['L2'] # Don't include the LinkPlus in the structure response (contains geolocation info)


class AuthStore:

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


class StructureHelper:

    def __init__(self, client):
        self.client = client

    def parse_structures(self):
        result = []
        root = self.client.get_structure_list()
        for structure_id in root['structures']:
            group_details = self.client.get_structure_details(structure_id)
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
    lw_auth = LWAuth()
    auth_store = AuthStore()

    if arguments['authenticate'] and arguments['<bearer>'] and arguments['<refresh>']:
        auth = lw_auth.refresh(arguments['<bearer>'], arguments['<refresh>'])
        auth_store.store_token(auth)
    elif arguments['list'] and arguments['all']:
        client = LWClient(auth_store.get_token())
        devices = StructureHelper(client).parse_structures()
        OutputWriter().print_output(devices, arguments['--file'])
    else:
        print 'Command not supported at this time'
        exit(1)



if __name__ == '__main__':
    main()
