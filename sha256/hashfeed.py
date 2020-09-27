import requests
import pymysql
from datetime import datetime,timedelta

db = pymysql.connect(host='localhost',user = 'root',password = 'W32.Blaster',db = 'feed',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

def db_insert(hash, hashtype, dt_string):
    baglanti.execute("""INSERT INTO filehash (hash, hashtype, dt_string) VALUES ("%s", "%s", "%s")""" % (hash,hashtype,dt_string))
    db.commit()

url = 'https://platform.socradar.com/api/hash_feed?days=1&key=a59e932a322e4686b5ead48ff8e874e2'


response = requests.get(url)
test = response.json()
test2 = (test[1])
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

n = 0
for i in test:
    test2 = (test[n])
    hash = test2["hash"]
    hashtype = test2["hash_type"]
    if hashtype == "md5s":
        print("No:",n,"Hash Type:", hashtype, ",","Hash:",hash)
        db_insert(hash, hashtype, dt_string)
    elif hashtype == "sha256s":
        print("No:",n,"Hash Type:", hashtype, ",","Hash:",hash)
        db_insert(hash, hashtype, dt_string)
    n = n + 1
