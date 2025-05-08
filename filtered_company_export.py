import requests
import json
import time
import datetime
from requests.adapters import HTTPAdapter, Retry
import csv

debug = 0
def Poll_Customobject(pageNumber):
    failCount = 0
    
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    ##This will reach out and grab all the USERS with STATUS within the account into an object and return it
    uri = "https://YOURURL.freshdesk.com/"
    uriRoute = "api/v2/companies"
    uriParams = "?page=" + str(pageNumber)
    url = uri + uriRoute + uriParams
    print(url)
    ##hardcoding this is stupid as hell, and shouldn't be here, yet here we are.
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
    return(response)

if debug == 1:
    Polled = Poll_Customobject('1')
    objectPoll = json.loads(Polled.text)
    print(objectPoll)
    quit()

page = 1

while page < 9:
    Polled = Poll_Customobject(page)
    ObjectPoll = json.loads(Polled.text)

    record_data = ObjectPoll

    headerRow = ''
    for keyName in record_data[0].keys():
        if headerRow == '':
            headerRow = keyName
        else:
            headerRow = headerRow + '|' + keyName

    iterations = len(record_data)
    count=0
    data_file = open('company_export_filtered.csv','w', encoding='utf-8')
    print(headerRow, file=data_file)

    for count in range(iterations):
        row_data = record_data[count]
        rowExtractData = ''
        for element in row_data:
            if rowExtractData == '':
                rowExtractData = row_data[element]
            else:
                rowExtractData = str(rowExtractData) + '|' + str(row_data[element])
        print(rowExtractData, file=data_file)
    page += 1