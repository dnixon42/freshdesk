import requests
import json
import time
import datetime
from requests.adapters import HTTPAdapter, Retry
import csv
import configparser

# Provide the accounts as a list of lists

accountInfo = [("","","")]

def getNextAccount():
    # This function will return the next row from the total accounts list and then pop it
    # once the list is empty, returns None, otherwise returns the row data
    if accountInfo:
        accountRow = accountInfo.pop(0)
    else:
        return None
    print("popped")
    return accountRow


def loadConfig(key):
    # Load the key value from the secrets file
    config = configparser.ConfigParser()
    config.read('freshdeskKeys.ini')
    return config['apiKeys'][key]

def Poll_Customobject(pageNumber, company_id = 0):
    # zero out the backoff period
    failCount = 0
    # configure the retries on connection failure
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    # take the incoming pageNumber as a Page Number starting at 1
    # take the company_id as the company_id passed to the function
    # return that page of contacts as the Requests.get object
    uri = "https://YOURURL.freshdesk.com/"
    uriRoute = "/api/v2/contacts"
    uriParams = "?page=" + str(pageNumber) + "&company_id=" + str(company_id)
    url = uri + uriRoute + uriParams
    # this loads the config each time it's run. Not efficient, but I'm not moving it now
    api_key = loadConfig("api_key")
    password = loadConfig("password")
    # try except block for any errors/backoffs/misses
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
    return(response)

def view_all_tickets():
    # write the header for the all contacts file
    data_file = open('contact_export.csv','a', encoding='utf-8')
    print("email|name|view_all_tickets", file=data_file)
    data_file.close()
    for x in range(1,6,1):
        Polled = Poll_Customobject(x)
        ObjectPoll = json.loads(Polled.text)
        record_data = ObjectPoll
        uri = "https://YOURURL.freshdesk.com/"
        uriRoute = "api/v2/contacts/"
        api_key = loadConfig("api_key")
        password = loadConfig("password")
        for row in record_data:
            url = uri + uriRoute + str(row['id'])
            response = requests.get(url, auth = (api_key, password))
            contactData = json.loads(response.text)
            if contactData["view_all_tickets"] == True:
                vat = True
            else:
                vat = False
            print(contactData["email"], "|",contactData["name"], "|", vat, file=data_file)
    data_file.close()

def fileInit():
    data_file = open('all_contacts_export.csv','w', encoding='utf-8')
    print("account name|location|contact email|contact name", file=data_file)
    data_file.close()

def all_EM_customer_contacts(accountValue):
    spins = 1
    print(accountValue[1])
    allContactDataRaw = Poll_Customobject(spins, accountValue[1])
    allContactData = json.loads(allContactDataRaw.text)
    if allContactData:
        data_file = open('all_contacts_export.csv','a', encoding='utf-8')
        for contactData in allContactData:
            if "deleted" in contactData:
                print("Deleted contact ", accountValue[0], " ", contactData["email"])
            else:
                print(accountValue[0], "|", accountValue[2], "|",contactData["email"], "|", contactData["name"], file=data_file)
        data_file.close()
        spins += 1
        allContactData = Poll_Customobject(spins, accountValue[1])
    else:
        print("Done with " + str(accountValue[0]) + " " + str(accountValue[1]))    


count = 0
fileInit()

while True:
    accountValue = getNextAccount()
    if accountValue is None:
        print("No more accounts")
        quit()
    else:
        all_EM_customer_contacts(accountValue)


# print(Poll_Customobject(30).text)
exit()
# testing()

