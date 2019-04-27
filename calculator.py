print ("""
1. Toplama
2. Cikarma
3. Carpma
4. Bolme
""")

a = int(input("birinci sayi:"))
b = int(input("ikinci sayi:"))

islem = input("islem giriniz:")

if (islem == 1):
    print ("{} ile {} in toplmami {} dir.".format(a,b,a + b))

elif (islem == 2):
    print ("{} ile {} in cikarmasi {} dir.".format(a,b,a - b))

elif (islem == 3):
    print ("{} ile {} in carpimi {} dir.".format(a,b,a * b))

elif (islem == 4):
    print ("{} ile {} in bolmesi {} dir.".format(a,b,a / b))

else:
    print("gecersiz islem.")