import requests
import json
import time
import datetime
from datetime import datetime
from requests.adapters import HTTPAdapter, Retry
import csv
import configparser

def loadConfig(key):
    config = configparser.ConfigParser()
    config.read('freshdeskKeys.ini')
    return config['apiKeys'][key]

def Poll_Customobject():
    api_key = loadConfig("api_key")
    password = loadConfig("password")
    failCount = 0
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    ##This will reach out and grab all the USERS with STATUS within the account into an object and return it
    uri = "https://YOURURL.freshdesk.com/"
    uriRoute = "api/v2/custom_objects/schemas/YOURSCHEMA/records"
    uriParams = "?page_size=100"
    url = uri + uriRoute + uriParams
    
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
    return(response)
    

def Poll_TicketFields():
    api_key = loadConfig("api_key")
    password = loadConfig("password")
    failCount = 0
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    ##This will reach out and grab all the USERS with STATUS within the account into an object and return it
    uri = "https://edifecs.freshdesk.com/"
    uriRoute = "api/v2/ticket_fields"
    url = uri + uriRoute
    
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
    return(response)



