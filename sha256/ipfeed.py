import requests
import pymysql
import re
from datetime import datetime,timedelta

db = pymysql.connect(host='localhost',user = 'root',password = 'W32.Blaster',db = 'feed',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

def db_insert(ip, dt_string):
    baglanti.execute("""INSERT INTO ip (ip, dt_string) VALUES ("%s", "%s")""" % (ip,dt_string))
    db.commit()

def db_select_ip(ip):
    baglanti.execute("""SELECT ip FROM ip = ("%s")""" % ip)
    return baglanti.fetchall()


url = 'https://platform.socradar.com/api/ip_feed?days=1&key=a59e932a322e4686b5ead48ff8e874e2'

response = requests.get(url)
test = response.json()
test2 = (test["ipv4s"])
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
blacklist = ['127.0.0.1','0.0.0.0']
n = 0
xxx = 1
for i in test2:
    test3 = (test2[n])
    ip = test3["ip"]
    if ip not in blacklist and not ip.startswith('192.168.') and not ip.startswith('10.'):
        print("No:", xxx, "IP Address:", ip)
        db_insert(ip, dt_string)
        xxx = xxx + 1
    n = n + 1
