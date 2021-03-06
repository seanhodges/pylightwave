"""LW command tool - send commands to devices

Usage:
  lw-command.py authenticate <bearer> <refresh>
  lw-command.py set <featureid> <value>
  lw-command.py get <featureid>
  lw-command.py (-h | --help)
  lw-command.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import os
import yaml
from docopt import docopt

from pylightwave.auth import LWAuth
from pylightwave.client import LWClient
from pylightwave.support import AuthStore


def main():
    arguments = docopt(__doc__, version='1.0')
    auth_store = AuthStore()

    if arguments['authenticate'] and arguments['<bearer>'] and arguments['<refresh>']:
        lw_auth = LWAuth()
        auth = lw_auth.refresh(arguments['<bearer>'], arguments['<refresh>'])
        auth_store.store_token(auth)
    elif arguments['set'] and arguments['<featureid>'] and arguments['<value>']:
        client = LWClient(auth_store.get_token())
        client.set_feature_value(arguments['<featureid>'], arguments['<value>'])
    elif arguments['get'] and arguments['<featureid>']:
        client = LWClient(auth_store.get_token())
        print client.get_feature_value(arguments['<featureid>'])
    else:
        print 'Command not supported at this time'
        exit(1)


if __name__ == '__main__':
    main()
