import os
import sys
from PIL import Image
import struct

sz = os.path.getsize(sys.argv[1])
df = open(sys.argv[1], "rb")

header = df.read(3)
assert header in [b"CW\x00",b"CH\x00"] # CW\x00
is_cw = header == b"CW\x00"
width = df.read(1)[0]
height = df.read(1)[0]
df.read(2)

temp = bytearray()
raw = False
pixel = 0

def rgb444toi24(data):
	from io import BytesIO
	offset = 0
	outp = BytesIO()
	while offset<len(data):
		inp = struct.unpack("<H", data[offset:offset+2])[0]
		rgb = (((inp>>12)&0xf)<<4,((inp>>8)&0xf)<<4,((inp>>4)&0xf)<<4)
		outp.write(struct.pack("<BBB", *rgb))
		offset += 2
	return outp.getvalue()
	
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
		tp_out = struct.pack("<B", cnt)+next
		if not is_cw:
			tp_out = rgb444toi24(tp_out)
		temp += tp_out
		continue
	cpl = df.read(2)
	if not is_cw:
		cpl = rgb444toi24(cpl)
	temp += cpl*cnt
	
if is_cw:	
	Image.frombytes("RGB", (width, height), bytes(temp),"raw", "BGR;16", 0, 1).save(sys.argv[2])
else:
	Image.frombytes("RGB", (width, height), bytes(temp)).save(sys.argv[2])	
#open(sys.argv[2], "wb").write(temp)
	
