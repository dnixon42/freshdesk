import requests
import json
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from requests.adapters import HTTPAdapter, Retry
import logging
import configparser


def loadConfig(key, context):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[context][key]

##Call this to grab the user information. It returns in JSON
def Poll_Users():
    failCount = 0
    retries = Retry(total=10, backoff_factor=0.1, status_forcelist=(500, 502, 504))
    http = requests.Session()
    http.mount('https://', HTTPAdapter(max_retries=retries))
    ##This will reach out and grab all the USERS with STATUS within the account into an object and return it
    uri = "https://edifecs.freshcaller.com/"
    uriRoute = "api/v1/users"
    uriParams = "?page=1&per_page=1000"
    ##setting per_page to 1000 ensures you get all users, if you have more than 1000 then you'll need to paginate and pull
    url = uri + uriRoute + uriParams
    my_headers = {'X-Api-Auth': loadConfig('apiKey', 'apiKey'),'accept': 'application/json'}
    ##need to put the Auth token somewhere cleaner instead of here
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
    return(response)
    

def Poll_Teams():
    ##This will reach out and grab all the TEAMS within the account into an object and return it
    uri = "https://edifecs.freshcaller.com/"
    uriRoute = "/api/v1/teams"
    uriParams = "?per_page=1000"
    ##need this since the default return count is 10
    url = uri + uriRoute + uriParams
    my_headers = {'X-Api-Auth': loadConfig('apiKey', 'apiKey'),'accept': 'application/json'}
    ##need to put the Auth token somewhere cleaner instead of here too
    if debugOutput == 1:
        print("Making call")
    try:
        response = requests.get(url, headers=my_headers)
    except requests.exceptions.RequestException as err:
        print ("Something Else",err)
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)     
    
    row = json.loads(response.text)
    for x in row["teams"]:
        print(x['id'], " ", x['name'])

def firstEmailAlert():
    ##must be connected to the VPN for this to use
    if testing == 1:
        return()
    with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
        msg = MIMEText('Heads up! No one has been in queue for 5 minutes!')
        msg['Subject'] = 'Freshcaller 5 minute alert! Inbound Queue Empty!'
        msg['From'] = 'user@email.com'
        msg['To'] = 'user@email.com'
        try:
            server.starttls() # Secure the connection
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("mail successfully sent")
        except:
            print("Something went wrong emailing out")
            
def secondEmailAlert():
    ##must be connected to the VPN for this to use
    if testing == 1:
        return()
    with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
        msg = MIMEText('Heads up! No one has been in queue for over 10 minutes!')
        msg['Subject'] = 'Freshcaller 10 minute alert! Inbound Queue Empty!'
        msg['From'] = 'user@email.com'
        msg['To'] = 'user@email.com'
        try:
            server.starttls() # Secure the connection
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("mail successfully sent")
        except:
            print("Something went wrong emailing out")
            
def thirdEmailAlert():
    if testing == 1:
        return()
    ##must be connected to the VPN for this to use
    with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
        msg = MIMEText('Heads up! No one has been in queue for over 15 minutes!')
        msg['Subject'] = 'Freshcaller 15 minutes alert! Inbound Queue Empty!'
        msg['From'] = 'user@email.com'
        msg['To'] = 'user@email.com'
        try:
            server.starttls() # Secure the connection
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("mail successfully sent")
        except:
            print("Something went wrong emailing out")
            
def returnedEmailAlert():
    if testing == 1:
        return()
    ##must be connected to the VPN for this to use
    with smtplib.SMTP("smtp-mail.outlook.com", port) as server:
        msg = MIMEText('Heads up! No one has been in queue for over 15 minutes!')
        msg['Subject'] = 'Freshcaller 15 minutes alert! Inbound Queue Empty!'
        msg['From'] = 'user@email.com'
        msg['To'] = 'user@email.com'
        try:
            server.starttls() # Secure the connection
            server.login(user, password)
            server.sendmail(sender, receiver, msg.as_string())
            print("mail successfully sent")
        except:
            print("Something went wrong emailing out")

##Set testing to 1 to use the test data above to limit API calls, otherwise set to 0
testing = 0
##Set getTeams to 1 to grab and output the list of teams with IDs in the account
getTeams = 0
##This is the teamID that we need to use to determine the status of a specific queue for monitoring
teamID = int(loadConfig('teamid', 'team'))
print('Checking statuses for', teamID)
##set this to 1 in order to get a lot more stuff printed out about what's going on
debugOutput = 0
##This sets up the number of times that we've seen an empty queue in a row
iteration = 0
##just counting the execution loops
execLoops = 0
##Capturing the startup time
startTime = datetime.datetime.now()
##Zero out the initial cycles count
emptyCycles = 0
##Set up the Webhooks URL for teams

##Set up the SMTP stuff to be able to email alerts
port = 587
sender = loadConfig('sender', 'emailKeys')
receiver = loadConfig('receiver', 'emailKeys')
logging.basicConfig(level=logging.DEBUG)
user = loadConfig('username', 'emailKeys')
password = loadConfig('password', 'emailKeys')

def usersDebug():
    response = Poll_Users()
    userPoll = json.loads(response.text)
    for person in userPoll['users']:
            print(person['name'],person['teams'],person['status'],teamID)
    quit()

while True:
    if getTeams == 1:
        Poll_Teams()
        quit()
    
    try:
        userPoll_obj = Poll_Users()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    userPoll = json.loads(userPoll_obj.text)
    ##Zero out the variables
    offlineAgents = 0
    onlineAgents = 0
    deletedCount = 0
    activeCallAgents = 0
    acwAgents = 0
    for person in userPoll['users']:
        if person['deleted'] == False:
            if person['status'] == 0:
                if debugOutput == 1:
                    print(person['name'], '-> offline', person['status'])
                    print(person['teams'])
                offlineAgents += 1
            elif person['status'] == 1:
                for userTeam in person['teams']:
                    if userTeam['id'] == teamID:
                        print(person['name'], '-> online', [person['status']])
                        onlineAgents += 1
            elif person['status'] == 2:
                for userTeam in person['teams']:
                    if userTeam['id'] == teamID:
                        print(person['name'], '-> active', [person['status']])
                        activeCallAgents += 1
            elif person['status'] == 3:
                acwAgents += 1
            else:
                print(person['name'], '-> status -> ', person['status'])
        else:
            deletedCount += 1

    print('Agents offline ->', offlineAgents)
    print('Agents online ->', onlineAgents)
    print('Agents on active calls ->', activeCallAgents)
    print('Agents in ACW ->', acwAgents)
    availableAgents = onlineAgents + activeCallAgents + acwAgents
    print('--------------------------------------------')
    print('All Available Agents ->', availableAgents)
    
    if availableAgents == 0:
        if iteration == 0:
            timeEmptyStart = datetime.datetime.now()
        iteration += 1
        print('Nobody available in the queue for the last ', iteration * 10, ' seconds')
        emptyCycles += 1
    elif availableAgents > 0:
        if iteration == 0:
            print('After ', iteration * 60, ' seconds, engineers are available')
            for person in userPoll['users']:
                if person['status'] == 1:
                    for userTeam in person['teams']:
                        if userTeam['id'] == teamID:
                            print(person['name'], '-> is online')
        iteration = 0
        timeEmptyStart = None
    if iteration == 6:
        print('Nobody in queue for over a minute')
    elif iteration == 30:
        print('URGENT: Nobody in queue for 5 minutes, please check statuses')
        firstEmailAlert()
    elif iteration == 60:
        print('ACTION REQUIRED: No one in queue for over 10 minutes')
        secondEmailAlert()
    elif iteration == 90:
        print('CRITICAL ACTION REQUIRED: No one in queue for over 15 minutes')
        thirdEmailAlert()

    execLoops += 1   
    print(datetime.datetime.now(), ' running for ', datetime.datetime.now() - startTime, ' empty user iteration: ', iteration, ' number of loops: ', execLoops)
    print(datetime.datetime.now(), ' ', emptyCycles, ' total checks with noone in queue')
    print('--------------------------------------------')
    print('============================================')
    time.sleep(10)
