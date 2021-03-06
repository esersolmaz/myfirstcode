from csv import reader
from datetime import datetime
import pymysql
import configparser
import json
import requests

config = configparser.ConfigParser()
config.read("../../../config.ini")

SIEM_IP = config.get("SIEM", "IP")
KEY = config.get("SIEM", "KEY")
DB_IP = config.get("DATABASE", "IP")
DB_USER = config.get("DATABASE", "USERNAME")
DB_PASSWORD = config.get("DATABASE", "PASSWORD")
CTI_URL = config.get("CTI","FILE_URL")

db = pymysql.connect(host=DB_IP,user = DB_USER,password = DB_PASSWORD,db = 'feed',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

BASE_URL = "https://" + SIEM_IP + "/api/reference_data/sets/bulk_load/ICD_SOCRADAR_FILEHASH?"

headers = {
    'SEC': KEY
}

def db_insert(hash,firstseeddate,lastseeddate,date_time,tags):
    baglanti.execute("""INSERT INTO filehash (hash,firstseeddate,lastseeddate,date_time,tags) VALUES ("%s","%s","%s","%s","%s")""" % (hash,firstseeddate,lastseeddate,date_time,tags))
    db.commit()


confirmedurl = (CTI_URL)
print(confirmedurl)
myfile = requests.get(confirmedurl)
open("/Users/user/PycharmProjects/myfirstcode/SOCRadar-Recommended-Block-Hash.csv", 'wb').write(myfile.content)

# read csv file as a list of lists
with open('/Users/user/PycharmProjects/myfirstcode/SOCRadar-Recommended-Block-Hash.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    n = 1
now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
filelist = []
n = 1
try:
    for i in list_of_rows:
        feedsatir = (list_of_rows[n])
        print(feedsatir)
        hash = (feedsatir[0])
        firstseendate = (feedsatir[1])
        lastseendate = (feedsatir[2])
        tags = (feedsatir[3])
        db_insert(hash,firstseendate,lastseendate,date_time,tags)
        filelist.append(hash)
        n = n + 1
finally:
    payload = filelist
    url = BASE_URL
    json_data = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()
    #print(json.dumps(json_data, indent=2))