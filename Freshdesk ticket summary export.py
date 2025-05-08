import requests
import json
import time
import datetime
from requests.adapters import HTTPAdapter, Retry

retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
http = requests.Session()
http.mount('https://', HTTPAdapter(max_retries=retries))
##This will reach out and grab all the USERS with STATUS within the account into an object and return it
uri = "https://YOURURL.freshdesk.com/"
uriRoute = "api/v2/search/tickets"
uriParams =  '?query="status:2 OR status:3 OR status:4"'
url = uri + uriRoute + uriParams

api_key = "x"
password = "x"

##need to put the Auth token somewhere cleaner instead of here
print("Making call")
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

    
##print(response.text)

ResponseJson = json.loads(response.text)
print(ResponseJson['total'])

for row in ResponseJson['results']:
    print(row['id'])
    print(row['status'])
