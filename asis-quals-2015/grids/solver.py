import math
import socket
import numpy as np
from scipy.spatial import ConvexHull

def CVArea(points):
	hull = ConvexHull(points)
	verts = hull.vertices.tolist()
	newpoints = []
	for v in verts:
		newpoints.append(points[v])
	print "old ", points, " np ", newpoints
	return PolygonArea(newpoints)	

# Area of Polygon using Shoelace formula
# http://en.wikipedia.org/wiki/Shoelace_formula
# FB - 20120218
# corners must be ordered in clockwise or counter-clockwise direction
def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def recv_until(st):
  ret = ""
  log = open("log.txt", "a")
  while st not in ret:
    r = s.recv(10)
    if r is None:
       exit(0)
    ret += r
    if "rapidly" in ret:
	print "wrong answer"
	exit(0)
    log.write(ret)
    log.flush()
  log.close()
  return ret

s = socket.create_connection(("217.218.48.84", 12434))

r = recv_until("?")
s.send("yes\n")

while True:
	q = recv_until("?")
	lines = q.split("\n")
	for l in lines:
		if l.startswith("["):
			question = l
			break

	print question
	a = eval(question)
	area = CVArea(a)
	print area
	s.send(str(area)+"\n")

