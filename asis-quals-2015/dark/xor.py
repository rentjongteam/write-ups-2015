import sys

f1 = open(sys.argv[1], "rb").read()
f2 = open(sys.argv[2], "rb").read()
f3 = open(sys.argv[3], "wb")

def rev(x):
	m = "%02x" % ord(x)
	n = m[1] + m[0]
	return int(n, 16)

res = ""
ctr = 0 
resx = ""
for i in range(0, len(f1)):
	resx =  chr(rev(f1[i]) ^ rev(f2[i]))+ resx
	if ctr==15:
		res += resx
		resx = ""
		ctr = 0
		continue
	ctr += 1

f3.write(res)
f3.close()
