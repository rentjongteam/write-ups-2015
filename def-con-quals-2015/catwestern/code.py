import socket
import struct
import os

def q(a):
  return struct.pack("I", a)

def recv_until(st):
    ret = ""
    while st not in ret:
        ret += s.recv(1)
        #print ret
    return ret


s = socket.create_connection(("catwestern_631d7907670909fc4df2defc13f2057c.quals.shallweplayaga.me", 9999))

regs = recv_until("bytes: \n")


ww = open("test.asm", "w")
ww.write("bits 64\n")

bytecount = 0

for line in regs.split("\n"):
    print line
    if "=" in line:
        a,b = line.split("=")
        ww.write("mov " +a +"," + b+"\n")
    if "bytes" in line:
        bc = line[line.index("send ")+ 5:]
        print bc
        bc = bc[:bc.index(" ")]
        bytecount = int(bc)

print "receiving ", bytecount

a = ""
while len(a)<bytecount:
    a += s.recv(1)

print "LEN ", len(a)

print a.encode("hex")

if ord(a[-1])==0xc3:
    a = a[:-1]


for c in a:
    ww.write("db 0x%x\n" % ord(c))

ww.close()

os.system("nasm test.asm")

with open("test", "rb") as f:
    binx = f.read()

os.system("cp template code")


print "update code ", len(binx)

with open("code", "r+b") as f:
    f.seek(0x4ba)
    f.write(binx)

    
os.system("gdb -q ./code  < gdb-script  > out.txt")

with open("out.txt", "r") as f:
    m = f.readlines()


for i in range(0, len(m)):
    if "()" in m[i]:
        start = i+1
        break

res = ""
for r in m[start:]:
    if r.startswith("rip"):
        continue
    if r.startswith("rsp"):
        continue
    if r.startswith("rbp"):
        continue

    if r.startswith("r"):
        r = r.strip()
        ab,c = r.split("\t")
        ab = '='.join(ab.split())
        print ab
        res += ab + "\n"
print "----"
print res
s.send(res)

print recv_until("\n")

