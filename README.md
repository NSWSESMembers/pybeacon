# NSW SES Beacon Login Handler

This Python module was created to streamline the acquisition of credentials to access Beacon's frontend and API, as well as handling some common job and messaging operations.

```
>>> from pybeacon import beacon_auth

>>> BEACON_URL = 'https://beacon.ses.nsw.gov.au'
>>> USERNAME = '4xxxxxxx'
>>> PASSWORD = 'xxx'

>>> pickled_cookies = beacon_auth.get_frontend_cookies(USERNAME, PASSWORD, BEACON_URL)
<pickled CookieJar>

>>> api_access_token = beacon_auth.get_api_token(USERNAME, PASSWORD, BEACON_URL)
{'accessToken': token, 'expiresAt': '2020-11-27T00:00:00.000Z'}

```

The module provides two auth-related functions: `get_api_token` and `get_frontend_cookies`. BEACON_URL must point to either Prod or Train Beacon.

## Usage
### Auth
* *USERNAME* - string
    * Identity username
* *PASSWORD* - string
    * Identity password
* *BEACON_URL* - string, optional
    * If undefined, defaults to Prod Beacon (`https://beacon.ses.nsw.gov.au`).

#### `beacon_auth.get_api_token`

To make a request to the Beacon API, first acquire a token.

```
from pybeacon import beacon_auth
import requests

token = beacon_auth.get_api_token(USERNAME, PASSWORD, BEACON_URL)
```

The token is returned as a dictionary along with the expiration time. It is **highly** recommended that this token be cached to reduce load on the identity server.

Pass the token to the Beacon API in the Authorization header of your request:

```
headers = {"Authorization": "Bearer " + token.get('accessToken')}
response = requests.get('https://apibeacon.ses.nsw.gov.au/Api/v1/Jobs/xxxxxx', headers=headers)
```

#### `beacon_auth.get_frontend_cookies`

To make a request to the Beacon frontend, first acquire session cookies and unpickle them.

```
from pybeacon import beacon_auth
import requests
import pickle

cookies = pickle.load(beacon_auth.get_frontend_cookies(USERNAME, PASSWORD, BEACON_URL))
```

The unpickled cookies are represented as a CookieJar object. Again, it is **highly** recommended that these cookies be cached to reduce load on the identity server.

Pass these cookies to the Beacon frontend using the `cookies` parameter.

```
response = requests.get('https://beacon.ses.nsw.gov.au/Jobs/', cookies=cookies)
```

---
### Jobs
Job functions generally take 3 parameters:
* *ACCESS_TOKEN* - string
    * This comes from the response of `beacon_auth.get_api_token`
    * E.g. `token.get('accessToken')`
* *JOB_ID* - string
    * This can take one of two forms: 12345678 or 1234-5678
    * Leading zeroes will be stripped
* *BEACON_API_URL* - string, optional
    * If undefined, defaults to Prod Beacon (`https://beaconapi.ses.nsw.gov.au`).
    * The provided token must match the specified environment e.g. to retrieve a job from Train Beacon, the token must have been issued by Train Identity.

#### `jobs.acknowledge_job`

To acknowledge a job, first get a token (hopefully from persistent storage), then call jobs.acknowledge_job().

```
from pybeacon import beacon_auth
import requests

token = beacon_auth.get_api_token(USERNAME, PASSWORD, BEACON_URL)

job = jobs.acknowledge_job(token.get('accessToken'), JOB_ID, BEACON_API_ENDPOINT)
```

The JSON response will contain the new status of the job (generally "Active"), and will be deserialised into a dictionary (not JSON like the example below) with the following schema:

```
{
    "Id": 2,
    "Name": "Active",
    "Description": "Job is under active management"
}
```

### `jobs.get_job`

To get the details of a job, first get a token (hopefully you've already persisted one somewhere), then call jobs.get_job().

```
from pybeacon import beacon_auth
import requests

token = beacon_auth.get_api_token(USERNAME, PASSWORD, BEACON_URL)

job = jobs.get_job(token.get('accessToken'), JOB_ID, BEACON_API_URL)
```

The JSON response from the API will be deserialised into a dictionary (not JSON like the example below) with the following schema:

```
{
    "Id": 123456,
    "Identifier": "0012-3456",
    "Sequence": 0,
    "FloodAssistanceJob": false,
    "ReferringAgency": null,
    "ReferringAgencyReference": null,
    "EmergencyOrder": null,
    "SituationOnScene": "Leaking roof",
    "EvacuationRequired": false,
    "PeopleInundated": 0,
    "PeopleExtricated": 0,
    "PeopleEvacuated": 0,
    "CreatedOn": "2020-09-04T12:00:23",
    "CreatedBy": {
        "Id": 2140,
        "FirstName": "Call",
        "LastName": "Taker",
        "FullName": "Call Taker",
        "Gender": 2,
        "RegistrationNumber": "40000000"
    },
    "CallerFirstName": "P",
    "CallerLastName": "Sherman",
    "ICEMSIncidentIdentifier": null,
    "ContactCalled": true,
    "CallerPhoneNumber": "0400123456",
    "ContactFirstName": null,
    "ContactLastName": null,
    "ContactPhoneNumber": null,
    "EntityAssignedTo": {
        "Id": 150,
        "Code": "KOG",
        "Name": "Kogarah",
        "Latitude": 0.0,
        "Longitude": 0.0,
        "EntityTypeId": 1,
        "HeadquartersStatusTypeId": 2,
        "ParentEntity": {
            "Id": 283,
            "Code": "MTZ",
            "Name": "Metro Zone"
        },
        "AriaCodeType": {
            "Id": 2,
            "Name": "Metropolitan",
            "Description": null
        },
        "AriaCode": null,
        "CadCode": "SES502"
    },
    "LGA": "GEORGES RIVER",
    "Sector": null,
    "JobPriorityType": {
        "Id": 4,
        "Name": "General",
        "Description": "General Response"
    },
    "TaskingCategory": 0,
    "JobType": {
        "ParentId": 1,
        "Id": 1,
        "Name": "Storm",
        "Description": "Storm Job"
    },
    "JobStatusType": {
        "Id": 8,
        "Name": "Finalised",
        "Description": "Job Finalised"
    },
    "Tags": [
        {
            "Id": 29,
            "Name": "Leaking Roof",
            "CreatedOn": "2014-09-18T13:59:36",
            "CreatedBy": 1,
            "TagGroupId": 6
        }
    ],
    "Address": {
        "GnafId": "GANSW1234567890",
        "Latitude": -33.39000,
        "Longitude": 151.1000,
        "Type": null,
        "Flat": null,
        "Level": null,
        "StreetNumber": "42",
        "Street": "WALLABY WAY",
        "Locality": "SYDNEY",
        "PostCode": "2000",
        "PrettyAddress": "42 WALLABY WAY, SYDNEY, NSW",
        "AdditionalAddressInfo": "X George Street"
    },
    "LastModified": "2020-09-05T18:58:00",
    "LastModifiedBy": {
        "Id": 2140,
        "FirstName": "Call",
        "LastName": "Taker",
        "FullName": "Call Taker",
        "Gender": 2,
        "RegistrationNumber": "40012345"
    },
    "JobStatusTypeHistory": [
        {
            "Type": 1,
            "Name": "New",
            "Description": "Send Message was selected.",
            "Timelogged": "2020-09-04T12:00:23",
            "CreatedOn": "2020-09-04T12:00:23",
            "CreatedBy": {
                "Id": 2140,
                "FirstName": "Call",
                "LastName": "Taker",
                "FullName": "Call Taker",
                "Gender": 2,
                "RegistrationNumber": "40012345"
            }
        }
    ],
    "PermissionToEnterPremises": true,
    "HowToEnterPremises": null,
    "Event": null,
    "JobReceived": "2020-09-04T12:00:23",
    "Reconnoitered": false,
    "AgenciesPresent": [],
    "FloodAssistance": null,
    "Type": "Storm",
    "PrintCount": 0
}   
```
