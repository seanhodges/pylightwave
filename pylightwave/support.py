import os
import yaml

class AuthStore:

    def store_token(self, auth):
        with open('.auth.yaml', 'w') as file_handle:
            yaml.safe_dump(auth, file_handle, default_flow_style=False, \
                    encoding='utf-8', allow_unicode=True)


    def get_token(self):
        if os.path.isfile('.auth.yaml'):
            with open('.auth.yaml', 'r') as stream:
                return yaml.load(stream, Loader=yaml.FullLoader)
        else:
            raise 'Please authenticate first :)'

