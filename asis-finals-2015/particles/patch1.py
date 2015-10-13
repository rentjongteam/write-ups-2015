import sys



def patch(origname, patchname, outname):
	a = open(patchname, "rb")
	p1 = a.read()

	i1 = p1.index("206 Part")
	i2 = p1.index("\r\n\r\n", i1)

	bb = "Content-Range: bytes "
	i3 = p1.index(bb)
	i4 = p1.index("/", i3)

	crange = p1[i3+len(bb):i4].split("-")

	content = p1[i2+4:]
	fr,to = int(crange[0]), int(crange[1])

	print fr,to

	print content.encode("hex")

	b = open(origname, "rb")
	odata = b.read()
	ndata = odata[:fr] + content + odata[to+1:]
	
	wr = open(outname, "wb")
	wr.write(ndata)
	wr.close()


def patch2(origname, patchname, outname):

	b = open(origname, "rb")
	odata = b.read()
	
	a = open(patchname, "rb")
	p1 = a.read()

	start = 0
	while True:
		bb = "Content-range: bytes "
		i3 = p1.find(bb, start)
		if i3==-1:
			break
		start = i3 + len(bb)

		i4 = p1.index("/", i3)
		i5 = p1.index("\r\n\r\n", i4) + 4

		crange = p1[i3+len(bb):i4].split("-")

		print crange
		fr,to = int(crange[0]), int(crange[1])
		lx = to-fr + 1

		content = p1[i5:i5+lx]

		print content

		odata = odata[:fr] + content + odata[to+1:]

	wr = open(outname, "wb")
	wr.write(odata)
	wr.close()

		
	
patch("orig.bin", "stream2", "out1.bin")
patch("out1.bin", "stream4", "out2.bin")
patch("out2.bin", "stream6", "out3.bin")
patch2("out3.bin", "stream8", "out4.bin")
patch2("out4.bin", "stream10", "out5.bin")

	
