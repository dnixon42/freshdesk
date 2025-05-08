import requests
import json
import time
import datetime
from requests.adapters import HTTPAdapter, Retry


retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
http = requests.Session()
http.mount('https://', HTTPAdapter(max_retries=retries))
##This will reach out and grab all the USERS with STATUS within the account into an object and return it
uri = "https://YOURURL.freshcaller.com/"
uriRoute = "api/v1/users"
uriParams = "?per_page=1000"
##need this since the default return count is 10
url = uri + uriRoute + uriParams
## gotta get this from your Freshcaller instance
my_headers = {'X-Api-Auth': 'x','accept': 'application/json'}
print("Making call")
try:
    response = http.get(url, headers=my_headers)
except requests.exceptions.RequestException as err:
    print ("Something Else",err)
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)

    
    
print(response.text)
ObjectPoll = json.loads(response.text)

record_data = ObjectPoll["users"]

headerRow = ''
for keyName in record_data[1].keys():
    if headerRow == '':
        headerRow = keyName
    else:
        headerRow = headerRow + '|' + keyName

iterations = len(record_data)
count=0
data_file = open('freshcaller_user.csv','w', encoding='utf-8')
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
