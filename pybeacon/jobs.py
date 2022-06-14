import datetime
import json
import re
import requests
from datetime import datetime, timedelta

# Sanitise job ID to be passed to /Api/v1/Jobs/xxxxxxxx or /Api/v1/Messages
def format_job_id(job_id):
    if re.search('\d{4}-\d{4}', job_id):
        return job_id.replace('-', '').lstrip('0')
    elif re.search('\d{1,8}', job_id):
        return job_id.lstrip('0')


# Return the specified job as an object
def get_job(access_token, job_id, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    job_id = format_job_id(job_id)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/Jobs/{}'.format(job_id),
                            headers=headers)
    return response.json()


# Acknowledge the specified job, returns new status
# Example response: {"Id":2,"Name":"Active","Description":"Job is under active management"}
def acknowledge_job(access_token, job_id, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):
    job_id = format_job_id(job_id)
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.post(beacon_api_url + '/Api/v1/Jobs/{}/Acknowledge'.format(job_id),
                             headers=headers)
    return response.json()

# Cancels the specified job, returns job details
# Example response: {"Id":2,"Name":"Active","Description":"Job is under active management"}
def cancel_job(access_token, job_id, beacon_api_url="https://apitrainbeacon.ses.nsw.gov.au"):
    job_id = format_job_id(job_id)
    headers = {'Authorization': 'Bearer {}'.format(access_token), 'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'Text':'Bulk Cancel','Date': datetime.now().isoformat()}
    response = requests.post(beacon_api_url + '/Api/v1/Jobs/{}/Cancel'.format(job_id),headers=headers,data=body)
    return response.json()

# q - Search job data
# hq - HQ ID
# start_date - datetime
# end_date - datetime

def format_datetime(start_date=datetime.now()):
    return start_date.strftime("%Y-%m-%dT%H:%M:%S")

def search_jobs(access_token, q=None, hq=None, start_date=None, end_date=None, beacon_api_url="https://apibeacon.ses.nsw.gov.au"):

    query = "";
    
    if(q != None):
        query += "q={}&".format(q)
        
    if(hq != None):
        query += "hq={}&".format(hq)
        
    if(start_date != None):
        query += "startdate={}&".format(format_datetime(start_date))
        
    if(end_date != None):
        query += "enddate={}&".format(format_datetime(end_date))
    
    if(query == ""):
        return None
    
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    response = requests.get(beacon_api_url + '/Api/v1/Jobs/Search?{}'.format(query),
                             headers=headers)
    return response.json()

# Returns a sitrep for the past X hours
def job_history_sitrep(access_token, hq, hours=72):
    now = datetime.now()
    now = now - timedelta(hours=hours)
    response = search_jobs(access_token, hq=hq, start_date=now)
    
    total_jobs = response["TotalItems"]
    outstanding_jobs = 0
    active_jobs = 0
    tasked_jobs = 0
    complete_jobs = 0
    referred_jobs = 0

    general_jobs = 0
    priority_jobs = 0
    immedate_jobs = 0
    life_threatening_jobs = 0

    results = response["Results"]
    
    areas={}
    
    for i in results:
        status = i["JobStatusType"]["Name"]
        if(status != "Finalised"):
            outstanding_jobs += 1
            if(status == "Active"):
                active_jobs += 1
            elif(status == "Tasked"):
                tasked_jobs += 1
            elif(status == "Complete"):
                complete_jobs += 1
            elif(status == "Referred"):
                referred_jobs += 1
                
        priority = i["JobPriorityType"]["Name"]
        
        if(priority == "General"):
            general_jobs += 1
        elif(priority == "Priority"):
            priority_jobs += 1
        elif(priority == "Immediate"):
            immedate_jobs += 1
        elif(priority == "Rescue"):
            life_threatening_jobs += 1
         
        suburb = i["Address"]["Locality"]
        
        if suburb in areas:
            areas[suburb] = areas[suburb] + 1
        else:
            areas[suburb] = 1
                 
    data = {
        "Total": total_jobs,
        "Outstanding": outstanding_jobs,
        "JobStatusType": {
            "Active": active_jobs,
            "Tasked": tasked_jobs,
            "Complete": complete_jobs,
            "Referred": referred_jobs
        },
        "JobPriorityType": {
            "General": general_jobs,
            "Priority": priority_jobs,
            "Immediate": immedate_jobs,
            "LifeThreatening": life_threatening_jobs
        },
        "Suburbs": sorted(areas.items(), key=lambda x: x[1], reverse=True)
    }
    
    return data;