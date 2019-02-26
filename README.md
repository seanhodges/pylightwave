# pylightwave

!!! Work in progress !!!

A basic Python library for Lightwave "v2" LinkPlus API.

## Usage

This project comes with some simple command-line tools that demonstrate the usage of the library.

You must authenticate before you can send commands, obtain a bearer token and refresh token from here: https://my.lightwaverf.com/settings/general/api

Then use the tokens to generate a full access token for use with the client. As below:

```python
#!/usr/bin/env python

from pylightwave.auth import LWAuth
from pylightwave.client import LWClient

lw_auth = LWAuth()
tokens = lw_auth.authenticate('<bearer_token>', '<refresh_token>')
lw_client = LWClient(tokens)
print lw_client.get_feature_details('<feature_id>')

