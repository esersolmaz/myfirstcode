import configparser
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

import sys
import json
from thehive4py.api import TheHiveApi
from thehive4py.models import CaseObservable


api = TheHiveApi('http://10.6.5.157:9000', 'eEBuNfc36ccy2Nk4OOdv+xOGIydptbmV')

config = configparser.ConfigParser()
config.read("config.ini")

SIEM_IP = config.get("SIEM", "IP")
KEY = config.get("SIEM", "KEY")


QRADAR_BASE_URL = "https://" + SIEM_IP + "/api/siem/offenses?filter=status%3DOPEN"
THEHIVE_BASE_URL = "http://10.6.5.157:9000/api/case"


qradar_headers = {
    'Content-Type': 'application/json',
}

thehive_headers = {
    'Authorization': 'Bearer eEBuNfc36ccy2Nk4OOdv+xOGIydptbmV',
    'Content-Type': 'application/json',
}

r_qradar = requests.get(url=QRADAR_BASE_URL, params=qradar_headers, auth=HTTPBasicAuth('eser.solmaz', 'W32.Bugbear170'),verify=False)


n = 0
data = r_qradar.json()
print(data[0])

for i in data:
    x = (data[n])
    description = x.get('description')
    offense_source = x.get('offense_source')
    start_timestamp = x.get('start_time')
    start_time = datetime.fromtimestamp(start_timestamp/1000.0)
    last_timestamp = x.get('last_persisted_time')
    last_time = datetime.fromtimestamp(last_timestamp/1000.0)
    offense_id = x.get('id')
    print("Offense Source: ",offense_source,",","Offence Name: ",description,",","Start Time: ",start_time,",","Last Time: ",last_time)
    offense_id = str(offense_id)
    offense_title = offense_id + "-" + offense_source

    xxx = {
                'title': offense_title,
                'description': "Offense ID: " + offense_id + " Offense Source : " + offense_source,
        }
    r_thehive = requests.post(url=THEHIVE_BASE_URL, headers={'Authorization': 'Bearer eEBuNfc36ccy2Nk4OOdv+xOGIydptbmV'}, data=xxx ,verify=False)
    data2 = r_thehive.json()
    thehive_caseid = data2.get('id')

    xxx2 = {
                'dataType': "ip",
                'data': offense_source,
                'tlp': 1,
                'ioc': True,
                'sighted': True,
                'message': "Test2",


        }


    r_thehive2 = requests.post(url= "http://10.6.5.157:9000/api/case/:84803832/artifact",headers={'Authorization': 'Bearer eEBuNfc36ccy2Nk4OOdv+xOGIydptbmV'}, data=xxx2,verify=False)
    data3 = r_thehive2.json()
    print(data3)
    print("data3 :",data3)

    print(thehive_caseid)

    # Init the CaseObservable object
    ip_observable = CaseObservable(dataType='ip', data=offense_source, tlp=1, ioc=True, sighted=True, )

    # Call the API
    response = api.create_case_observable(thehive_caseid, ip_observable)
    print(data2)
    print(type(data2))
    n = n + 1






