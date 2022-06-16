a = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
lenx = (int(len(a)))
print(lenx)
print(type(lenx))

xx = int(lenx / 2)
print(xx)

aa = a[xx:10:1]
bb = a[(xx - 1)::-1]
bb.reverse()
cc =  aa + bb
print(aa)
print(bb)
print(cc)