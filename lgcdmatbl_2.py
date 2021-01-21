import struct
import os
import sys
from io import BytesIO

if len(sys.argv) < 5:
	print(f"Not enough arguments! usage: {sys.argv[0]} file offset_hex count output", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
imgoffs = int(sys.argv[2], 16)
imgcnt = int(sys.argv[3])

fd.seek(imgoffs)

outp = bytearray()

curoffs = 0

for cn in range(imgcnt):
    outtmp = bytearray()
    imgoffs = struct.unpack("<L", fd.read(4))[0]
    if imgoffs > sz:
        continue
        
    icuroffs = fd.tell()
    
    fd.seek(imgoffs)
        
    width = fd.read(1)[0]
    widthtype = fd.read(1)[0]
    height = fd.read(1)[0]
    heighttype = fd.read(1)[0]
        
    tsz = ((int(width)*int(height))*2)
    
    if widthtype == 0x80 and heighttype == 0x80:
        while len(outtmp) < tsz:
            tt = struct.unpack("<H", fd.read(2))[0]
            
            compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
            cnt = tt % 0x8000 # 15 bit: length
                        
            if not compressed:
                outtmp += fd.read(cnt*2)
            else:
                bit = fd.read(2)
                outtmp += bit*cnt
                
        outp += outtmp[:tsz]
    elif widthtype == 0x00 and heighttype == 0x00:
        outp += fd.read(tsz)
    
    fd.seek(icuroffs)
    
open(sys.argv[4],"wb").write(outp)

