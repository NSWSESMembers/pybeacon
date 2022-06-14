import requests
import json

# Return the specified job as an object
def get_contact_group(access_token, contact_group_id, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/ContactGroups/{}'.format(contact_group_id),
                            headers=headers)
    return response.json()

# Get formatted list of recipients for sending sms from a contact group
def get_recipients_from_contact_group(access_token, contact_group_id, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/ContactGroups/{}'.format(contact_group_id),
                            headers=headers).json()
    contacts = response["ContactGroupContactMappings"]

    result = []
    
    for i in contacts:
        data = {
            "Description": i["Contact"]["FullName"],
            "Recipient": i["Contact"]["Detail"],
            "ContactTypeId": i["Contact"]["ContactTypeId"],
        }
        result.append(data)

    return json.dumps(result)
    