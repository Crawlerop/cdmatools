import os
import sys
import struct

if len(sys.argv) < 5:
	print(f"Not enough arguments! usage: {sys.argv[0]} file width height output", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

fda = bytearray(fd.read())

width = int(sys.argv[2])
height = int(sys.argv[3])

bit_header = struct.pack("<HH", 0x8000+width, 0x8000+height)

print(bit_header)

outp = bytearray()

#sys.exit(1)

tg_offs = fda.find(bit_header)

while tg_offs != -1:
	print(tg_offs)
	toutp = bytearray()
	fd.seek(tg_offs+4)
	
	while len(toutp)<=(width*height)*2:
		tt = struct.unpack("<H", fd.read(2))[0]
		
		compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
		cnt = tt % 0x8000 # 15 bit: length
		
		if not compressed:
				toutp += fd.read(cnt*2)
		else:
			bit = fd.read(2)
			toutp += bit*cnt
	
	outp += toutp
	tg_offs = fda.find(bit_header, tg_offs+4)
    
open(sys.argv[4],"wb").write(outp)

