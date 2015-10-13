def xor(a, b):
    res = ""
    la = len(a)
    lb = len(b)
    if (la>lb):
        ll = lb
    else:
        ll = la
    for i in range(0, ll):
        res +=  chr(ord(a[i])^ord(b[i]))
    return res

def xor3(a, b, c):
    res = ""
    la = len(a)
    lb = len(b)
    if (la>lb):
        ll = lb
    else:
        ll = la
    for i in range(0, ll):
        res +=  chr(ord(a[i])^ord(b[i])^c)
    return res


def xorc(a, c):
    res = ""
    for i in range(0, len(a)):
        res +=  chr(ord(a[i])^c)
    return res

a = open("_aAAAc_", "wb")

line = ['','','','','']

line[3] = "hgyGxW"
line[2] = xor(line[3], "GrCRed")
line[1] = xor3(line[3], "Vc4LTy", 0x23)
line[0] = xor(line[1], "iKWoZL")
line[4] = xor(xor(xorc(line[3], 0x23), "PhfEni"), line[2])

all = '\n'.join(line)

def validate(x):
    line = x.split("\n")
    print xor(line[0], line[1])=="iKWoZL" #0x400d24
    print xor3(line[3], line[1], 0x23)=="Vc4LTy"
    print xor(line[2], line[3])=="GrCRed" #compare @0x400dce
    print xor(xor3(line[4], line[3], 0x23), line[2])=="PhfEni" #compare @0x400e3d
    print line[3]=="hgyGxW"

validate(all)

print len(all)

a.write(all)

a.close()
