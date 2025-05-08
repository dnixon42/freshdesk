import requests
import json
import time
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter, Retry
import csv
from dateutil.relativedelta import relativedelta

## Set up the URI and the route
uri = "https://YOURURL.freshdesk.com/"
agentRoute = "api/v2/tickets"


## establish counters
count = 0
rowCount = 0



## Poll_Agent takes an INT as a page number and then hits the API are returns the json
## of users from that page.
def Poll_Tickets(company_id):
    failCount = 0
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    uriParams = "?include=stats&company_id=" + str(company_id)
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
    print(response)
    return(response)

#provide company ID here
company_id = 0
tickets = json.loads(Poll_Tickets(company_id).text)
print(tickets)
count = 0
for row in tickets:
    print(row)
    # count += 1
    # print(count, row["id"])
    