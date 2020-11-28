# NSW SES Beacon Login Handler

This Python module was created to streamline the acquisition of credentials to access Beacon's frontend and API.

```
>>> from pybeacon import beacon_auth

>>> BEACON_URL = 'https://beacon.ses.nsw.gov.au'
>>> USERNAME = '4xxxxxxx'
>>> PASSWORD = 'xxx'

>>> pickled_cookies = beacon_auth.get_frontend_cookies(BEACON_URL, USERNAME, PASSWORD)
<pickled CookieJar>

>>> api_access_token = beacon_auth.get_api_token(BEACON_URL, USERNAME, PASSWORD)
{'accessToken': token, 'expiresAt': '2020-11-27T00:00:00.000Z'}

```

The module provides two functions: `get_api_token` and `get_frontend_cookies`. BEACON_URL must point to either Prod or Train Beacon.

## Usage
### `get_api_token`

To make a request to the Beacon API, first acquire a token.

```
from pybeacon import beacon_auth
import requests

token = beacon_auth.get_api_token(BEACON_URL, USERNAME, PASSWORD)
```

The token is returned as a dictionary along with the expiration time. It is **highly** recommended that this token be cached to reduce load on the identity server.

Pass the token to the Beacon API in the Authorization header of your request:

```
headers = {"Authorization": "Bearer " + token.get('accessToken')}
response = requests.get('https://apibeacon.ses.nsw.gov.au/Api/v1/Jobs/xxxxxx', headers=headers)
```

### `get_frontend_cookies`

To make a request to the Beacon frontend, first acquire session cookies and unpickle them.

```
from pybeacon import beacon_auth
import requests

cookies = pickle.load(beacon_auth.get_frontend_cookies(BEACON_URL, USERNAME, PASSWORD))
```

The unpickled cookies are represented as a CookieJar object. Again, it is **highly** recommended that these cookies be cached to reduce load on the identity server.

Pass these cookies to the Beacon frontend using the `cookies` parameter.

```
response = requests.get('https://beacon.ses.nsw.gov.au/Jobs/', cookies=cookies)
```

