import json
import requests
import pickle
from requests_html import HTMLSession
from urllib.parse import urlparse

# Prod or Train Beacon can be specified here
BEACON_URL = 'https://beacon.ses.nsw.gov.au'
USERNAME = '4xxxxxxx'
PASSWORD = 'xxx'


# Helper to determine which Identity instance to use
def _get_identity_env(response):
    parsed_uri = urlparse(response.url)
    return '{uri.scheme}://{uri.hostname}'.format(uri=parsed_uri)


def _do_login(beacon_url, username, password):
    session = HTMLSession()

    try:
        response = session.get(beacon_url,
                               headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'},
                               )
        identity_url = _get_identity_env(response)

        if response.html.find('.login-box'):
            # Extract modelJson for xsrf token, strip leading and trailing LR and spaces
            model_json = response.html.find('#modelJson', first=True).text.replace('&#13;', '').strip()

            # Extract loginUrl and xsrf token
            model_json = json.loads(model_json)
            login_url = model_json['loginUrl']
            xsrf = model_json['antiForgery']['value']
            del model_json

        else:
            raise requests.exceptions.InvalidURL

        # Build login form data
        data = {
            'idsrv.xsrf': xsrf,
            'username': username,
            'password': password
        }

        # Perform login
        response = session.post(identity_url + login_url, data)

        # Delete object containing credentials
        del data

        if response.status_code == 200:
            # Get OAuth redirectUrl
            oauthRedirectUrl = response.html.find('form', first=True).attrs['action']
            # Get OAuth callback form hidden fields
            formInputs = response.html.find('input')

            # Build OAuth callback form data
            data = {}
            for i in formInputs:
                data[i.element.name] = i.element.value

            # Finally perform OAuth callback
            # response = session.post(oauthRedirectUrl, data)

            return session.post(oauthRedirectUrl, data)

        else:
            raise requests.exceptions.RequestException

    except requests.exceptions.RequestException as e:
        print(e)


def get_api_token(beacon_url, username, password):
    response = _do_login(beacon_url, username, password)

    bearer_token = {
        'accessToken': response.html.search('self.accessToken = \'{}\'')[0],
        'expiresAt': response.html.search('self.expiresAt = \'{}\'')[0]
    }
    return bearer_token


def get_frontend_cookies(beacon_url, username, password):
    response = _do_login(beacon_url, username, password)

    # Can be loaded into a new session with `session.cookies.update(pickle.load(cookies))`
    cookies = pickle.dumps(response.cookies)
    return cookies

# if __name__ == "__main__":
#     do_login(BEACON_URL, USERNAME, PASSWORD)
