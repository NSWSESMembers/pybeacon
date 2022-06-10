import json
import requests


def get_message(access_token, message_id: str, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/Messages/{}'.format(message_id),
                            headers=headers)
    return response.json()

# Description can be contacts name
# ContactTypeId is method for sending eg Email-1, SMS-2
def generateContactJSON(phone):
    return { "Description": phone, "Recipient": phone, "ContactTypeId" : 2 }

# Sends sms to a list of phone numbers
# Contacts should be a string list of phone numbers
def send_sms(access_token, messageText : str, contacts: list, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    
    recipients = []
    
    for contact in contacts:
        recipients.append(generateContactJSON(contact));
    
    data = {
        "MessageText": messageText,
        "Recipients": recipients
    }
    
    data = json.dumps(data)
    
    headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
    response = requests.post(beacon_api_url + '/Api/v1/Messages/',
                            headers=headers, data=data)
    return response.json()