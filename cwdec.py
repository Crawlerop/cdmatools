import os
import sys
from PIL import Image
import struct

sz = os.path.getsize(sys.argv[1])
df = open(sys.argv[1], "rb")

assert df.read(3) == b"CW\x00" # CW\x00
width = df.read(1)[0]
height = df.read(1)[0]
df.read(2)

temp = bytearray()
raw = False
pixel = 0

while df.tell()<sz:
	cnt = df.read(1)[0]
	if cnt == 0xff and (not raw or pixel >= width): 
		raw = False
		pixel = 0
		continue
	if cnt == 0x00 and (not raw or pixel >= width): 
		raw = True
		pixel = 0
		continue

	if raw:
		pixel += 1
		next = df.read(1)
		temp += struct.pack("<B", cnt)+next
		continue
	cpl = df.read(2)
	temp += cpl*cnt
	
Image.frombytes("RGB", (width, height), bytes(temp),"raw", "BGR;16", 0, 1).save(sys.argv[2])
#open(sys.argv[2], "wb").write(temp)
	
