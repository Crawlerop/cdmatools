import os
import sys
import struct

if len(sys.argv) < 5:
	print(f"Not enough arguments! usage: {sys.argv[0]} file width height output", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

width = int(sys.argv[2])
height = int(sys.argv[3])

outp = bytearray()

while fd.tell() < sz:
    tt = struct.unpack("<H", fd.read(2))[0]

    if tt == (0x8000+width) or tt == (0x8000+height):
        continue                        
                        
    compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
    cnt = tt % 0x8000 # 15 bit: length
                            
    if not compressed:
        outp += fd.read(cnt*2)
    else:
        bit = fd.read(2)
        outp += bit*cnt
    
open(sys.argv[4],"wb").write(outp)

