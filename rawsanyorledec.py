import os
import sys

sz = os.path.getsize(sys.argv[1])
df = open(sys.argv[1], "rb")
of = open(sys.argv[2], "wb")
plte = open(sys.argv[3], "rb")

pts = []
b = True
while b != b"":
	if b == True:
		b = plte.read(2)
		continue
	pts.append(b)
	b = plte.read(2)

while df.tell()<sz:
	cnt = df.read(1)[0]
	if cnt in [0xff,0x0]: continue
	adt = pts[df.read(1)[0]]
	of.write(adt*cnt)