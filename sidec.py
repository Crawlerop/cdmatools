import os
import sys
from PIL import Image
import struct

sz = os.path.getsize(sys.argv[1])
df = open(sys.argv[1], "rb")
pts = []

assert df.read(4) == b"SI\x10\x00" # SI\x10\x00
assert df.read(2) == b"\x02\x00" # Always 2?
width = struct.unpack("<H", df.read(2))[0] # Width
height = struct.unpack("<H", df.read(2))[0] # Height
df.read(3)
palette_size = df.read(1)[0]+1
df.read(2)

def rgb565toi24(data):
	from io import BytesIO
	offset = 0
	outp = BytesIO()
	while offset<len(data):
		inp = struct.unpack("<H", data[offset:offset+2])[0]
		rgb = (((inp & 0xF800) >> 8), ((inp & 0x07E0) >> 3), ((inp & 0x001F) << 3))
		outp.write(struct.pack("<BBB", *rgb))
		offset += 2
	return outp.getvalue()

for _ in range(palette_size):
	pts.append(rgb565toi24(df.read(2)))

temp = bytearray()

while df.tell()<sz:
	cnt = df.read(1)[0]
	print(cnt)
	if cnt in [0xff,0x0]: continue
	p_bit = df.read(1)[0]	
	adt = pts[p_bit]
	temp += adt*cnt
	
Image.frombuffer("RGB", (width, height), bytes(temp)).save(sys.argv[2])
	
