import requests
import json
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter, Retry
import csv
from dateutil.relativedelta import relativedelta

## Set up the URI and the route
uri = "https://YOURURL.freshdesk.com/"
agentRoute = "api/v2/agents"

## establish counters
count = 0
rowCount = 0

## email addresses to omit

## Poll_Agent takes an INT as a page number and then hits the API are returns the json
## of users from that page.
def Poll_Agent(pageNumber):
    failCount = 0
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    uriParams = "?page=" + str(pageNumber)
    url = uri + agentRoute + uriParams

    api_key = "x"
    password = "x"

    ## Basic error handling
    try:
        response = requests.get(url, auth = (api_key, password))
    except requests.exceptions.RequestException as err:
        print ("Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    return(response)

agentCount = 0
delta = 0
while count < 30:
    agentRawData = Poll_Agent(count+1)
    if agentRawData == None:
        quit()
    agentJson = json.loads((agentRawData.text))
    for i in agentJson:
        if (i["type"] != "collaborator") and (i["occasional"] != True) and (i["deactivated"] != True):
            rowCount = rowCount + 1
            if i["contact"]["last_login_at"] is not None:
                agentCount = agentCount + 1
                print("name:",i["contact"]["name"],":email:",i["contact"]["email"],":isactive:",i["contact"]["active"],":last login:","no login")
            else:
                agentCount = agentCount + 1
                print("name:",i["contact"]["name"],":email:",i["contact"]["email"],":isactive:",i["contact"]["active"],":last login:",i["contact"]["last_login_at"])
    count = count + 1