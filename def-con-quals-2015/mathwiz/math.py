import socket
import struct
import re

def q(a):
  return struct.pack("I", a)

def recv_until(st):
  ret = ""
  while st not in ret:
    ret += s.recv(1)
    print ret
  return ret

s = socket.create_connection(("mathwhiz_c951d46fed68687ad93a84e702800b7a.quals.shallweplayaga.me", 21249))


digits = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE"]


while True:
	st = recv_until("\n")

	print st.encode("hex")

	st = st.replace("=\n", "")

	st = st.replace("[", "(")
	st = st.replace("]", ")")
	st = st.replace("{", "(")
	st = st.replace("}", ")")
	st = st.replace("^", "**")



	for i in range(0, len(digits)):
		st = st.replace(digits[i], str(i))


	if re.match(".*[A-Za-z].*", st):
		print st
		print recv_until("\n")
		exit(0)

	


	print st
	res = eval(st)
	s.send(str(res) + "\n")
