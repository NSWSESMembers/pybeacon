import json
import requests


def get_message(access_token, message_id: str, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/Messages/{}'.format(message_id),
                            headers=headers)
    return response.json()


# ContactTypeId-1 Email
# ContactTypeId-2 SMS
# ContactTypeId-3 Hard Call
# ContactTypeId-4 Hard Call
# ContactTypeId-5+ Unknown

def generate_email_contact_JSON(name, email):
    return { "Description": name, "Recipient": email, "ContactTypeId" : 1 }

def generate_sms_contact_JSON(name, phone):
    return { "Description": name, "Recipient": phone, "ContactTypeId" : 2 }

# Send message to provided recipients
# Generate items using generate_email_contact_JSON() and generate_sms_contact_JSON()
def send_message(access_token, messageText : str, recipients: list, beacon_api_url="https://apibeacon.ses.nsw.gov.au", reply_to="", operational=False):
    
    data = {
        "MessageText": messageText,
        "Recipients": recipients,
        "Operational": operational
    }
    
    # Currently broken, messagerecipienttypeid gets changed to 8 when posted, not sure why
    if(reply_to != ""):
        data["ReplyToAddresses"] = [{
            "Detail": reply_to,
            "MessageRecipientTypeId": 2
        }]
    
    data = json.dumps(data)
    
    headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/json'}
    response = requests.post(beacon_api_url + '/Api/v1/Messages/',
                            headers=headers, data=data)
    return response.json()