import re
import requests

# Sanitise job ID to be passed to /Api/v1/Jobs/xxxxxxxx
def format_job_id(job_id):
    if re.search('\d{4}-\d{4}', job_id):
        return job_id.replace('-', '').lstrip('0')
    elif re.search('\d{1,8}', job_id):
        return job_id.lstrip('0')


# Return the specified job as an object
def get_job(access_token, job_id, api_endpoint="https://apibeacon.ses.nsw.gov.au"):

    job_id = format_job_id(job_id)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(api_endpoint + '/Api/v1/Jobs/{}'.format(job_id),
                            headers=headers)
    return response.json()


# Acknowledge the specified job, returns new status
# Example response: {"Id":2,"Name":"Active","Description":"Job is under active management"}
def acknowledge_job(access_token, job_id, api_endpoint="https://apibeacon.ses.nsw.gov.au"):

    job_id = format_job_id(job_id)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.post(api_endpoint + '/Api/v1/Jobs/{}/Acknowledge'.format(job_id),
                            headers=headers)
    return response.json()
