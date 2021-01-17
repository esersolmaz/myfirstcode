from csv import reader
from datetime import datetime
import pymysql
import configparser
import json
import requests
import socket

config = configparser.ConfigParser()
config.read("../../../config.ini")

SIEM_IP = config.get("SIEM", "IP")
KEY = config.get("SIEM", "KEY")
DB_IP = config.get("DATABASE", "IP")
DB_USER = config.get("DATABASE", "USERNAME")
DB_PASSWORD = config.get("DATABASE", "PASSWORD")
CTI_URL = config.get("CTI","IP_URL")

db = pymysql.connect(host=DB_IP,user = DB_USER,password = DB_PASSWORD,db = 'feed',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

BASE_URL = "https://" + SIEM_IP + "/api/reference_data/sets/bulk_load/ICD_SOCRADAR_IP?"

headers = {
    'SEC': KEY
}

def db_insert(ipaddress,firstseeddate,lastseeddate,date_time,tags):
    baglanti.execute("""INSERT INTO ip (ipaddress,firstseeddate,lastseeddate,date_time,tags) VALUES ("%s","%s","%s","%s","%s")""" % (ipaddress,firstseeddate,lastseeddate,date_time,tags))
    db.commit()

def db_select_ip(ipaddress):
    baglanti.execute("""SELECT ip FROM ip = ("%s")""" % ipaddress)
    return baglanti.fetchall()

def db_truncate_table():
    baglanti.execute("""TRUNCATE TABLE ip""" )
    db.commit()

def valid_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except:
        return False

confirmedurl = (CTI_URL)
print(confirmedurl)
myfile = requests.get(confirmedurl)
open("/Users/user/PycharmProjects/myfirstcode/SOCRadar-Attackers-Recommended-Block-IP.csv", 'wb').write(myfile.content)

# read csv file as a list of lists
with open('/Users/user/PycharmProjects/myfirstcode/SOCRadar-Attackers-Recommended-Block-IP.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    n = 1
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
db_truncate_table()
iplist = []
n = 1
try:
    for i in list_of_rows:
        feedsatir = (list_of_rows[n])
        ipaddress = (feedsatir[0])
        firstseendate = (feedsatir[1])
        lastseendate = (feedsatir[2])
        tags = (feedsatir[3])
        n = n + 1
        vvv = valid_ip(ipaddress)
        if vvv == True:
            iplist.append(ipaddress)
            db_insert(ipaddress,firstseendate,lastseendate,date_time,tags)
            print(n," ",ipaddress," ","database kaydi yapılmistir.")

finally:
    payload = iplist
    url = BASE_URL
    json_data = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()
    #print(json.dumps(json_data, indent=2))