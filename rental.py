"""
Project Name : Rental Project
Version: 1.1
Author : Eser SOLMAZ
Date : 09.03.2020
Changes 1.1;
credit card number is encrypted and written to the database.
"""
import pymysql
from datetime import datetime,timedelta
import re
from cryptography.fernet import Fernet

db = pymysql.connect(host='localhost',user = 'root',password = 'qwe123',db = 'rental',charset = 'utf8mb4',cursorclass = pymysql.cursors.DictCursor)
baglanti = db.cursor()

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

write_key()
key = load_key()
f = Fernet(key)


#Bisiklet ve Martı Kirlama için kullanıclan class dır.
class kiralama():
    def __init__(self,isim,soyisim,telefon,kiralamabitis):
        self.isim = isim
        self.soyisim = soyisim
        self.telefon = telefon
        self.kiralamabitis = kiralamabitis

    def bisikletkiralama(self,isim,soyisim,telefon,kiralamabitis,ucret):
        baglanti.execute("""INSERT INTO hareketler (isim, soyisim, telefon, aractipi, aracno, kiralamabaslangic, kiralamabitis, ucret) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.isim, self.soyisim, self.telefon, "bisiklet","1",date_time2,self.kiralamabitis,ucret))
        db.commit()

    def bisikletkiralama_kk(self,isim,soyisim,telefon,kiralamabitis,ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno):
        baglanti.execute("""INSERT INTO hareketler (isim, soyisim, telefon, aractipi, aracno, kiralamabaslangic, kiralamabitis, ucret, kkisim, kksoyisim, kkgecerliliktarihi, kkcvv, kkno) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.isim, self.soyisim, self.telefon, "bisiklet","1",date_time2,self.kiralamabitis,ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno))
        db.commit()

    def martikiralama(self,isim,soyisim,telefon,kiralamabitis,ucret):
        baglanti.execute("""INSERT INTO hareketler (isim, soyisim, telefon, aractipi, aracno, kiralamabaslangic, kiralamabitis, ucret) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.isim, self.soyisim, self.telefon, "marti","1",date_time2,self.kiralamabitis,ucret))
        db.commit()

    def martikiralama_kk(self,isim,soyisim,telefon,kiralamabitis,ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno):
        baglanti.execute("""INSERT INTO hareketler (isim, soyisim, telefon, aractipi, aracno, kiralamabaslangic, kiralamabitis, ucret, kkisim, kksoyisim, kkgecerliliktarihi, kkcvv, kkno) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")""" % (self.isim, self.soyisim, self.telefon, "marti","1",date_time2,self.kiralamabitis,ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno))
        db.commit()

class odeme():
    def __init__(self,ilkzaman,sonzaman):
        self.ilkzaman = ilkzaman
        self.sonzaman = sonzaman

class nakit(odeme):
    def __init__(self,x1,x2):
        self.x1 = x1
        self.x2 = x2

    def nakitucrethesaplama(a,b):
        if secim == ("M"):
            ucret = ()
            ucret = (a * martigun) + (b / 3600 * martisaat)
            return ucret
        elif secim == ("B"):
            ucret = ()
            ucret = (a * bisikletgun) + (b / 3600 * bisikletsaat)
            return ucret

class kredikarti(odeme):
    def __init__(self,ilkzaman,sonzaman,soyisim,gecerliliktarihi,cvv):
        self.ilkzaman = ilkzaman
        self.sonzaman = sonzaman
        self.isim = input("İsim Giriniz: ")
        self.soyisim = input("Soyisim Giriniz: ")
        self.gecerliliktarihi = input("AY/YIL olarak geçerlilik tarihi giriniz:")
        self.cvv = int(input("CVV giriniz: "))


    def kkucrethesaplama(a,b):
        if secim == ("M"):
            ucret = ()
            ucret = (a * martigun) + (b / 3600 * martisaat)
            return ucret
        elif secim == ("B"):
            ucret = ()
            ucret = (a * bisikletgun) + (b / 3600 * bisikletsaat)
            return ucret

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
time = now.strftime("%H:%M:%S")
date_time = datetime.now()
date_time2 = datetime.now()
dateformat = "%Y-%d-%m %H:%M:%S"
karsilamamesaji = ("Rental Programına Hoş Geldiniz.", day,month,year,time)
martisaat = 10
martigun = 100
bisikletsaat = 5
bisikletgun = 50

print(karsilamamesaji)

secim = input("Marti kiralama için (M) harfine, Bisiklet kiralamak için (B) Harfine basınız: ")
isim = input("İsim Giriniz: ")
soyisim = input("Soyisim Giriniz: ")
#Telefon Numarası Dogrulama
while True:
    telefon = input("Telefon Numarası Giriniz: ")
    if re.match('(05\d{8})',telefon):
        break
    print("Telefon numarası 10 hane olarak 05331234567 şekilde girilmelidir. Lütfen tekrar deneyiniz.")

#Tarih Dogrulama
while True:
    kiralamabitis2 = input("Kiralama bitis (YIL-AY-GUN SAAT:DAKİKA:SANİYE) : ")
    if re.match('(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})',kiralamabitis2):
        kiralamabitis = datetime.strptime(kiralamabitis2, "%Y-%m-%d %H:%M:%S")
        break
    print("Kiralama bitis YIL-AY-GUN SAAT:DAKİKA:SANİYE şekilde girilmelidir. Lütfen tekrar deneyiniz.")
kiralamasure = kiralamabitis - now
odemetipi = input("Ödeme tipi nakit ise 'N' harfine kredi kartı ise 'K' harfine basınız: ")
print(kiralamasure.days)
print(kiralamasure.seconds)
x1 = float(kiralamasure.days)
x2 = float(kiralamasure.seconds)

xxx = kiralama(isim,soyisim,telefon,kiralamabitis)

if secim == ("B"):

        if odemetipi == ("N"):
            ucret = nakit.nakitucrethesaplama(x1,x2)
            xxx.bisikletkiralama(isim, soyisim, telefon, kiralamabitis, ucret)
            print("Sayın", isim, " ", soyisim, "firmamızı tercih ettiginiz için teşşekür ederiz.",ucret,"TL tahsilatı yapılmıştır.")

        elif odemetipi == ("K"):
            kkisim = input("İsim Giriniz: ")
            kksoyisim = input("Soyisim Giriniz: ")
            # CVV doğrulama
            while True:
                kkno2 = input("Kredi kartı numarası giriniz(1234-1234-1234-1234) :".encode())
                if re.match('(\d{4}\-\d{4}\-\d{4}\-\d{4})', kkno2):
                    break
                print("redi kartı numarası 1234-1234-1234-1234 gibi olmalıdır. Lütfen tekrar deneyiniz.")
            kkno3 = kkno2.encode()
            kkno = f.encrypt(kkno3)
            kkgecerliliktarihi = input("AY/YIL olarak geçerlilik tarihi giriniz:")
            # CVV doğrulama
            while True:
                kkcvv = input("CVV giriniz: ")
                if re.match('(\d{3})', kkcvv):
                    break
                print("CVV numarası 123 gibigirilmelidir. Lütfen tekrar deneyiniz.")

            ucret = nakit.nakitucrethesaplama(x1,x2)
            xxx.bisikletkiralama_kk(isim, soyisim, telefon, kiralamabitis, ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno)
            print("Sayın",isim," ",soyisim,"firmamızı tercih ettiginiz için teşşekür ederiz." ,ucret,"TL tahsilatı yapılmıştır.")

elif secim == ("M"):
        if odemetipi == ("N"):
            ucret = nakit.nakitucrethesaplama(x1,x2)
            xxx.martikiralama(isim, soyisim, telefon, kiralamabitis, ucret)
            print("Sayın", isim, " ", soyisim, "firmamızı tercih ettiginiz için teşşekür ederiz.",ucret,"TL tahsilatı yapılmıştır.")

        elif odemetipi == ("K"):
            kkisim = input("İsim Giriniz: ")
            kksoyisim = input("Soyisim Giriniz: ")
            # CVV doğrulama
            while True:
                kkno2 = input("Kredi kartı numarası giriniz(1234-1234-1234-1234) :")
                if re.match('(\d{4}\-\d{4}\-\d{4}\-\d{4})', kkno2):
                    break
                print("redi kartı numarası 1234-1234-1234-1234 gibi olmalıdır. Lütfen tekrar deneyiniz.")
            kkno3 = kkno2.encode()
            kkno = f.encrypt(kkno3)
            kkgecerliliktarihi = input("AY/YIL olarak geçerlilik tarihi giriniz:")
            # CVV doğrulama
            while True:
                kkcvv = input("CVV giriniz: ")
                if re.match('(\d{3})', kkcvv):
                    break
                print("CVV numarası 123 gibigirilmelidir. Lütfen tekrar deneyiniz.")

            ucret = nakit.nakitucrethesaplama(x1,x2)
            xxx.martikiralama_kk(isim, soyisim, telefon, kiralamabitis, ucret,kkisim,kksoyisim,kkgecerliliktarihi,kkcvv,kkno)
            print("Sayın",isim," ",soyisim,"firmamızı tercih ettiginiz için teşşekür ederiz." ,ucret,"TL tahsilatı yapılmıştır.")

