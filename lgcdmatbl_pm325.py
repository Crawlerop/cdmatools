import struct
import os
import sys
from io import BytesIO
from PIL import Image

if len(sys.argv) < 4:
	print(f"Not enough arguments! usage: {sys.argv[0]} file offset_hex output", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
imgoffs = int(sys.argv[2], 16)

fd.seek(imgoffs)

if not os.path.exists(f"{sys.argv[3]}/"):
	os.mkdir(f"{sys.argv[3]}/")
	
i_path = f"{sys.argv[3]}/"

curoffs = 0

imgcnt = struct.unpack("<L", fd.read(4))[0]

iof_sizes = []

for cn in range(imgcnt):
	fd.read(4)
	file_size = struct.unpack("<L", fd.read(4))[0]
	fd.read(4)
	
	file_name = fd.read(40).replace(b"\x00", b"").decode("ascii").replace(".bmp", "")

	iof_sizes.append({"fsz":file_size,"fname":file_name})

for ids in iof_sizes:
	
    outtmp = bytearray()
	
    temp = fd.read(2)
		
    if temp != b"\xcd\xcd":
	    fd.seek(fd.tell()-2)
	
    ibuf = BytesIO(fd.read(ids["fsz"]))
        
    width = ibuf.read(1)[0]

    widthtype = ibuf.read(1)[0]
    height = ibuf.read(1)[0]
    	
    heighttype = ibuf.read(1)[0]
    
    print(width, height)
            
    if widthtype == 0x80 and heighttype == 0x80:
        while ibuf.tell()<ids["fsz"]:
            tt = struct.unpack("<H", ibuf.read(2))[0]
            
            compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
            cnt = tt % 0x8000 # 15 bit: length
                        
            if not compressed:
                outtmp += ibuf.read(cnt*2)
            else:
                bit = ibuf.read(2)
                outtmp += bit*cnt
                
        Image.frombytes("RGB", (width, height), bytes(outtmp[:((width*height)*2)]),"raw", "BGR;16", 0, 1).save(f"{i_path}{ids['fname']}.png")
        
    elif widthtype == 0x00 and heighttype == 0x00:
        outtmp = ibuf.read(ids["fsz"]-4)
        Image.frombytes("RGB", (width, height), outtmp,"raw", "BGR;16", 0, 1).save(f"{i_path}{ids['fname']}.png")
    
    

