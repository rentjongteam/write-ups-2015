
def parse(m):
        n =  m.split("  ")
        nn = n[1] + " " + n[2]
        nn = nn.replace(" ", "")
        return nn.decode("hex")



def readfile(filename):
	with open(filename, "r") as f:
		data = f.readlines()

        inside = False
        res = ""
        for m in data:
                if m.startswith("==="):
                        inside = not inside
                        continue
                if inside:
                        if m.startswith("\t"):
                                res += parse(m)
        return res

#returns start, and data
def split(data):
        s1 = "Content-Range: bytes "
        s2 = "\r\n\r\n"
        n = data.index(s1)+len(s1)
        n2 = data.index(s2)
        line =  data[n:n2].split("-")
        pos =  int(line[0])
        resdata = data[n2+len(s2):]
        return (pos, resdata)

pnghead ="89504e470d0a1a0a0000000d49".decode("hex")


with open("output.png", "wb+") as f:
        f.write(pnghead)
        for i in range(0, 23):
                data = readfile(str(i))
                pos, rdata = split(data)
                print i, pos
                f.seek(pos)
                f.write(rdata)

                
