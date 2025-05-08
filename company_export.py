import requests
import json
import time
import datetime
from requests.adapters import HTTPAdapter, Retry
import csv


def Poll_Customobject(pageNumber):
    failCount = 0
    
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    ##This will reach out and grab all the USERS with STATUS within the account into an object and return it
    uri = "https://HARDCODED.freshdesk.com/"
    uriRoute = "api/v2/companies"
    uriParams = "?page=" + str(pageNumber)
    url = uri + uriRoute + uriParams
    print(url)
    ## TODO: Add the code to pull the key from the function after I refactor
    api_key = "x"
    password = "x"
    
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
    print(response.text)
    return(response)


count = 0
while True:
    print(count)
    if count == 0:
        data_file = open('company_export.csv','w', encoding='utf-8')
        print("id|name", file=data_file)
        data_file.close()
    elif count >= 860:
        quit()
    else:
        Polled = Poll_Customobject(count)
        ObjectPoll = json.loads(Polled.text)
        record_data = ObjectPoll
        for row in record_data:
            data_file = open('company_export.csv','a', encoding='utf-8')
            ## lazy pipe versus comma delimited. In my case pipe is never in the data set
            print(row['id'],'|',row['name'], file=data_file)
            ##print(row['id'],",",row['name'],",",row['description'])
            data_file.close()
    count += 1
