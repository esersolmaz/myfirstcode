players = [{'name':'gustavo','age':34},{'name':'mesut','age':33},{'name':'enner','age':32},{'name':'filip','age':31},{'name':'serdar','age':31},{'name':'serdar','age':30},{'name':'marcel','age':29},{'name':'pelkas','age':28},{'name':'nazim','age':28},{'name':'zajc','age':27},{'name':'mert','age':27},{'name':'ozan','age':27},{'name':'irfan','age':26},{'name':'crespo','age':25},{'name':'kim','age':25},{'name':'osayi','age':24},{'name':'atilla','age':24},{'name':'rossi','age':24},{'name':'murat','age':24},{'name':'altay','age':24},{'name':'mergin','age':24},{'name':'ferdi','age':22},{'name':'burak','age':22},{'name':'berke','age':22},{'name':'serhat','age':20},{'name':'cagatay','age':20},{'name':'arda','age':19},{'name':'ertugrul','age':19},{'name':'arda','age':17}]

deger = 0
futbolcusayisi = 0
yastoplam = 0
for i in players:
    d = i['age']
    yastoplam = d + yastoplam
    futbolcusayisi = futbolcusayisi + 1
print(yastoplam)
print(futbolcusayisi)
deger = yastoplam / futbolcusayisi
print(deger)