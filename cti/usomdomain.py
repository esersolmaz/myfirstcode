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


db = pymysql.connect(host=DB_IP,user = DB_USER,password = DB_PASSWORD,db = 'feed',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

BASE_URL = "https://" + SIEM_IP + "/api/reference_data/sets/bulk_load/ICD_USOM_ZARARLI_URL?"

headers = {
    'SEC': KEY
}

def db_insert(domain,date_time):
    baglanti.execute("""INSERT INTO usom_zararliurl (domain,date_time) VALUES ("%s","%s")""" % (domain,date_time))
    db.commit()

def db_truncate_table():
    baglanti.execute("""TRUNCATE TABLE usom_zararliurl""" )
    db.commit()



confirmedurl = ("https://www.usom.gov.tr/url-list.txt")
print(confirmedurl)
myfile = requests.get(confirmedurl)
open("/Users/user/PycharmProjects/myfirstcode/USOM_URL_LIST.TXT", 'wb').write(myfile.content)

# read csv file as a list of lists
with open('/Users/user/PycharmProjects/myfirstcode/USOM_URL_LIST.TXT', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    n = 1

now = datetime.now()
date_time = now.strftime("%Y-%m-%d %H:%M:%S")
domainlist = []
n = 1
try:
    for i in list_of_rows:
        feedsatir = (list_of_rows[n])
        domain = (feedsatir[0])
        n = n + 1
        db_insert(domain,date_time)
        domainlist.append(domain)

finally:
    payload = domainlist
    url = BASE_URL
    json_data = requests.post(url, data=json.dumps(payload), headers=headers, verify=False).json()
    print(json.dumps(json_data, indent=2))
