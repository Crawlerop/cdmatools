import os
import sys
import struct

sz = os.path.getsize(sys.argv[1])
df = open(sys.argv[1], "rb")
of = open(sys.argv[2], "wb")
plte = open(sys.argv[3], "rb")
width = int(sys.argv[4])

pts = []
b = True
while b != b"":
	if b == True:
		b = plte.read(2)
		continue
	pts.append(b)
	b = plte.read(2)

raw = False
#raw2 = False
cnto = 0

while df.tell()<sz:
	#print("b",hex(df.tell()))
	cnt = df.read(1)[0]
	if cnt == 0xff: 
		raw = False
		cnto = 0
		#raw2 = False
		continue
	if cnt == 0x00 and (not raw or cnto >= width): 
		#of.write(pts[cnt])
		#df.read(1)
		raw = True
		cnto = 0
		continue
	'''
	elif cnt == 0x00 and raw and not raw2:
		raw2 = True
		continue
	elif cnt != 0x00 and raw2:
		raw2 = False
	'''
	if raw:
		of.write(pts[cnt])
		cnto += 1
		#df.read(1)
		continue
	cpl = df.read(1)[0]
	if cpl > len(pts): 
		#print("perror")
		continue
	adt = pts[cpl]
	#print("a",hex(of.tell()))
	#if cpl == 0xc and cnt == 0xc:
		#of.write(adt*2)
	#lse:
	of.write(adt*cnt)