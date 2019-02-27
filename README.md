# pylightwave

!!! Work in progress !!!

A basic Python library for Lightwave "v2" LinkPlus API.

##  Tool usage

This project comes with some simple command-line tools that demonstrate how to use the library. Use `--help` to get usage help.

* lw-probe.py - Retrieve device and feature information (including feature ID's)
* lw-command.py - Send commands to device capabilities (features)
* lw-event.py - Listen to events from v2 devices

##  Library usage

You must authenticate before you can send commands, obtain a bearer token and refresh token from here: https://my.lightwaverf.com/settings/general/api

_Note:_ Likely you'll need to refresh your new token before first use.

Then use the tokens to generate a full access token for use with the client. Simple example below:

```python
#!/usr/bin/env python

from pylightwave.auth import LWAuth
from pylightwave.client import LWClient

lw_auth = LWAuth()
tokens = lw_auth.refresh('<bearer token>', '<refresh token>')
lw_client = LWClient(tokens)
print lw_client.get_feature_value('<feature id>')

