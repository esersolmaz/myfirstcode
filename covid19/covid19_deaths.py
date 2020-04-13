import requests
from csv import reader
from datetime import datetime,timedelta
import pymysql

db = pymysql.connect(host='localhost',user = 'root',password = '12345678',db = 'covid19',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

def db_insert_deaths(country, day, count):
    baglanti.execute(
        """INSERT INTO deaths (country, day, count) VALUES ("%s", "%s", "%s")""" % (country,day,count))
    db.commit()

def db_truncate_table():
    baglanti.execute("""TRUNCATE TABLE deaths""" )
    db.commit()


deathsurl = ("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
print(deathsurl)
myfile = requests.get(deathsurl)
open("time_series_covid_19_deaths_global.csv", 'wb').write(myfile.content)

db_truncate_table()

# read csv file as a list of lists
with open('/Users/user/PycharmProjects/myfirstcode/time_series_covid_19_deaths_global.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Pass reader object to list() to get a list of lists
    list_of_rows = list(csv_reader)
    n = 1


    for i in list_of_rows:
        x = (list_of_rows[n])
        nn = 0
        day = 1
        for ii in x:
            country = (x[1])
            y = (x[nn])
            if nn >= 4:
                if y != ("0"):
                    db_insert_deaths(country,day,y)
                    day = day + 1
            nn = nn + 1
        n = n + 1

