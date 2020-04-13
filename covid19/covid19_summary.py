import http.client
import json
import pymysql
from datetime import datetime,timedelta
import plotly.graph_objects as go
import numpy as N

db = pymysql.connect(host='localhost',user = 'root',password = '12345678',db = 'covid19',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

def db_insert(country, totalcases, newcases, activecases, criticalcases, recoveredcases, newdeaths,totaldeaths, day,datetime):
    baglanti.execute(
        """INSERT INTO summury (country, totalcases, newcases, activecases, criticalcases, recoveredcases, newdeaths, totaldeaths, day, datetime) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (
        country,totalcases,newcases,activecases,criticalcases,recoveredcases,newdeaths,totaldeaths,day,datetime))
    db.commit()

def db_insert_spread_rate(country,count, day, rate):
    baglanti.execute("""INSERT INTO spread_rate (country, count, day, rate) VALUES ("%s", "%s", "%s", "%s")""" % (country,count,day,rate))
    db.commit()

def db_update(totalcases, newcases, activecases, criticalcases, recoveredcases, newdeaths,totaldeaths, day, datetime, country):
    baglanti.execute(
        """UPDATE summury SET totalcases="%s", newcases="%s", activecases="%s", criticalcases="%s", recoveredcases="%s", newdeaths="%s", totaldeaths="%s", day="%s", datetime="%s" where country = '%s'""" % (
        totalcases,newcases,activecases,criticalcases,recoveredcases,newdeaths,totaldeaths,day,datetime,country))
    db.commit()

def db_deathrate_update(deathrate, country):
    baglanti.execute(
        """UPDATE summury SET deathrate="%s" where country = '%s'""" % (deathrate,country))
    db.commit()

def db_select_totalcases(country):
    baglanti.execute("""SELECT totalcases FROM summury where country = ("%s")""" % country)
    return baglanti.fetchall()

def db_select_status():
    baglanti.execute("""SELECT country,totalcases,activecases,criticalcases,recoveredcases,totaldeaths,deathrate FROM summury order by totalcases DESC LIMIT 0,200""")
    return baglanti.fetchall()

def db_confirmed_speed(country):
    baglanti.execute("""SELECT count FROM confirmed where country = ("%s")""" % country)
    return baglanti.fetchall()

def db_confirmed_speed2():
    baglanti.execute("""SELECT country FROM confirmed""")
    return baglanti.fetchall()

def db_confirmed_speed_sum(country):
    baglanti.execute("""SELECT count,day FROM confirmed where country = ("%s") order by count DESC LIMIT 1 """ % country)
    return baglanti.fetchall()

def db_spread_rate(country):
    baglanti.execute("""SELECT rate,count,day FROM spread_rate where country = ("%s") order by rate DESC LIMIT 50 """ % country)
    return baglanti.fetchall()

def db_spread_rate2():
    baglanti.execute("""SELECT country,rate,count,day FROM spread_rate order by rate DESC LIMIT 50 """)
    return baglanti.fetchall()

def db_deaths_speed(country):
    baglanti.execute("""SELECT count FROM deaths where country = ("%s")""" % country)
    return baglanti.fetchall()

def db_recovered_speed(country):
    baglanti.execute("""SELECT count FROM recovered where country = ("%s")""" % country)
    return baglanti.fetchall()

def db_truncate_table_spread_rate():
    baglanti.execute("""TRUNCATE TABLE spread_rate""" )
    db.commit()

conn = http.client.HTTPSConnection("covid-193.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "5745e20a36msh1abf560cc7a121bp1536ffjsn9c3739838bfa"
    }

conn.request("GET", "/statistics", headers=headers)
res = conn.getresponse()
data = res.read()
data2 = data.decode("utf-8")
json_string = data2
obj = json.loads(json_string)
response = obj["response"]
n = 0

print("""Covid-19 Uygulamasına Hoş Geldiniz.
Yeni vakaları çekmek için A harfina basınız.
Ülke durumlarını görmek için B harfina basınız.
Ülke bazlı veri görselleştirme C harfine basınız
Genel veri görselleştirme için D harfine basınız.
Yayılım hızını görmek için E harfine basınız.""")

secim = input("Secim harfini giriniz:")

if secim == ("A"):
    for i in response:
        x = (response[n])
        country = (x["country"])
        cases = (x["cases"])
        totalcases = (cases["total"])
        newcases = (cases["new"])
        activecases = (cases["active"])
        criticalcases = (cases["critical"])
        recoveredcases = (cases["recovered"])
        deaths = (x["deaths"])
        newdeaths = (deaths["new"])
        totaldeaths = (deaths["total"])
        deathrate = 100 * (totaldeaths / totalcases)
        day = (datetime.strptime(x["day"],"%Y-%m-%d"))
        datetime = (datetime.strptime(x["time"],"%Y-%m-%dT%H:%M:%S+00:00"))
        test = db_select_totalcases(country)
        a = (test[0])
        if (a["totalcases"]) == totalcases:
            print(country," yeni vaka yoktur.")
        elif (a["totalcases"]) < totalcases:
            db_update(totalcases, newcases, activecases, criticalcases, recoveredcases, newdeaths, totaldeaths,day, datetime, country)
            db_deathrate_update(deathrate,country)
            print(country," update yapilidi")
        n = n + 1
elif secim == ("B"):
    a = db_select_status()
    x = 0
    for i in a:

        n = (a[x])
        country = (n["country"])
        totalcases = (n["totalcases"])
        activecases = (n["activecases"])
        criticalcases = (n["criticalcases"])
        recoveredcases = (n["recoveredcases"])
        totaldeaths = (n["totaldeaths"])
        deathrate = (n["deathrate"])
        print("Country:",country,',',"Death Rate:",deathrate,',',"Total:",totalcases,',',"Active:", activecases,',',"Critical:",criticalcases,',',"Recovered:",recoveredcases,',',"Total Deaths:",totaldeaths)
        x = x + 1
elif secim == ("C"):
    country = (input("Country :"))
    a = db_confirmed_speed(country)
    b = db_deaths_speed(country)
    c = db_recovered_speed(country)
    x = 0
    countlist_confirmed = []
    countlist_deaths = []
    countlist_recovered = []
    daylist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38\
    ,38,39,40,41,42,43,44,45,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,\
    64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]

    for i in a:
        n = (a[x])
        count_confirmed = (n["count"])
        countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in b:
        nn = (b[x])
        count_deaths = (nn["count"])
        countlist_deaths.append(count_deaths)
        x = x + 1
    x = 0
    for i in c:
        nnn = (c[x])
        count_recovered = (nnn["count"])
        countlist_recovered.append(count_recovered)
        x = x + 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daylist, y=countlist_confirmed, name='Confirmed',
                             line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=countlist_deaths, name='Deaths',
                             line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=countlist_recovered, name='Recovered',
                             line=dict(color='green', width=4,
                                       dash='dash')
                             ))
    fig.update_layout(title='Covid-19 Case Count Matrix',
                      xaxis_title='Days',
                      yaxis_title='Case Count')
    fig.show()

elif secim == ("D"):

    a1 = db_confirmed_speed("Turkey")
    a2 = db_confirmed_speed("Italy")
    a3 = db_confirmed_speed("Germany")
    a4 = db_confirmed_speed("Korea, South")
    a5 = db_confirmed_speed("India")
    a6 = db_confirmed_speed("Spain")
    a7 = db_confirmed_speed("United Kingdom")
    a8 = db_confirmed_speed("US")
    a9 = db_confirmed_speed("France")
    a10 = db_confirmed_speed("Iran")
    x = 0
    a1_countlist_confirmed = []
    a2_countlist_confirmed = []
    a3_countlist_confirmed = []
    a4_countlist_confirmed = []
    a5_countlist_confirmed = []
    a6_countlist_confirmed = []
    a7_countlist_confirmed = []
    a8_countlist_confirmed = []
    a9_countlist_confirmed = []
    a10_countlist_confirmed = []
    daylist = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38\
    ,38,39,40,41,42,43,44,45,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,\
    64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80]

    for i in a1:
        n = (a1[x])
        count_confirmed = (n["count"])
        a1_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a2:
        n = (a2[x])
        count_confirmed = (n["count"])
        a2_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a3:
        n = (a3[x])
        count_confirmed = (n["count"])
        a3_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a4:
        n = (a4[x])
        count_confirmed = (n["count"])
        a4_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a5:
        n = (a5[x])
        count_confirmed = (n["count"])
        a5_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a6:
        n = (a6[x])
        count_confirmed = (n["count"])
        a6_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a7:
        n = (a7[x])
        count_confirmed = (n["count"])
        a7_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a8:
        n = (a8[x])
        count_confirmed = (n["count"])
        a8_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a9:
        n = (a9[x])
        count_confirmed = (n["count"])
        a9_countlist_confirmed.append(count_confirmed)
        x = x + 1
    x = 0
    for i in a10:
        n = (a10[x])
        count_confirmed = (n["count"])
        a10_countlist_confirmed.append(count_confirmed)
        x = x + 1

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daylist, y=a1_countlist_confirmed, name='Turkey',
                             line=dict(color='blue', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a2_countlist_confirmed, name='Italy',
                             line=dict(color='black', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a3_countlist_confirmed, name='Germany',
                             line=dict(color='violet', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a4_countlist_confirmed, name='S-Korea',
                             line=dict(color='pink', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a5_countlist_confirmed, name='India',
                             line=dict(color='grey', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a6_countlist_confirmed, name='Spain',
                             line=dict(color='brown', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a7_countlist_confirmed, name='UK',
                             line=dict(color='firebrick', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a8_countlist_confirmed, name='US',
                             line=dict(color='orange', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a9_countlist_confirmed, name='France',
                             line=dict(color='purple', width=4)))
    fig.add_trace(go.Scatter(x=daylist, y=a10_countlist_confirmed, name='Iran',
                             line=dict(color='green', width=4)
                             ))
    fig.update_layout(title='Covid-19 Confirmed Count',
                      xaxis_title='Day',
                      yaxis_title='Count')
    fig.show()

elif secim == ("E"):
    db_truncate_table_spread_rate()
    a = db_confirmed_speed2()
    countrylist = []
    x = 0
    for i in a:
        n = (a[x])
        country = (n["country"])
        countrylist.append(country)
        x = x + 1
    res = N.array(countrylist)
    unique_res = N.unique(res)

    x = 0
    for i in unique_res:
        n = (unique_res[x])
        a = db_confirmed_speed_sum(n)
        aa = (a[0])
        count = (aa["count"])
        day = (aa["day"])
        rate = count / day
        db_insert_spread_rate(n,count,day,rate)
        sonuc = db_spread_rate(n)
        #print(sonuc[0])
        x = x + 1
    a = db_spread_rate2()
    x = 0
    for i in a:
        aa = (a[x])
        country = (aa["country"])
        rate = (aa["rate"])
        count = (aa["count"])
        day = (aa["day"])
        print("Country :", country, ",", "Spread Rate : ",rate , "," ,"Day :", day , ",", "Count :", count)
        x = x + 1