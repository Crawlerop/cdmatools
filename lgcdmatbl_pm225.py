import struct
import os
import sys
from io import BytesIO
from PIL import Image
import string

if len(sys.argv) < 5:
	print(f"Not enough arguments! usage: {sys.argv[0]} file offset_hex count output", file=sys.stderr)
	sys.exit(1)

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
imgoffs = int(sys.argv[2], 16)
imgcnt = int(sys.argv[3])

'''

fnames = []

fd.seek(imgoffs+(imgcnt*4))

imgfindDone = False

isend = False

for _ in range(imgcnt):
	tmpname = ""
	if isend: break
	while True:
		tmpread = fd.read(1)
		if tmpread == b"\x00":
			if not imgfindDone:
				imgfindDone = True
			else:
				isend = True
			print(_, imgcnt)
			fnames.append(tmpname[:-4])
			break
		else:
			imgfindDone = False
		assert tmpread in string.printable.encode("utf-8"), f"{tmpread} not decodable"
		tmpname += tmpread.decode("ascii")
		
'''

fd.seek(imgoffs)

if not os.path.exists(f"{sys.argv[4]}/"):
	os.mkdir(f"{sys.argv[4]}/")
	
i_path = f"{sys.argv[4]}/"

curoffs = 0

for cn in range(imgcnt):
    outtmp = bytearray()
    nameoffs = struct.unpack("<L", fd.read(4))[0]        
    imgoffs = struct.unpack("<L", fd.read(4))[0]
    
    if imgoffs > sz:
        continue
        
    icuroffs = fd.tell()
    
    fd.seek(nameoffs)
    
    tmpnam = ""
    
    if nameoffs > sz:
        tmpnam = f"unknown_{cn}.bmp"
    else:	
    	tk = fd.read(1)
    	while tk != b"\0":
    		tmpnam += tk.decode("ascii")
    		tk = fd.read(1)
    
    tmpnam = tmpnam[:-4]
    
    fd.seek(imgoffs)
        
    isl = fd.read(4)
        
    size = struct.unpack("<L", isl)[0] - 4
    
    #print(size)
    
    dfxd = BytesIO(fd.read(size))
        
    width = dfxd.read(1)[0]
    widthtype = dfxd.read(1)[0]
    height = dfxd.read(1)[0]
    heighttype = dfxd.read(1)[0]
    
    #print(widthtype, heighttype)
        
    #tsz = ((int(width)*int(height))*2)
    
    if widthtype == 0x80 and heighttype == 0x80:
        while dfxd.tell()<size:
            tt = struct.unpack("<H", dfxd.read(2))[0]
            
            compressed = tt >> 15 # 1 bit: 0x0: Raw, 0x1: RLE
            cnt = tt % 0x8000 # 15 bit: length
                        
            if not compressed:
                outtmp += dfxd.read(cnt*2)
            else:
                bit = dfxd.read(2)
                outtmp += bit*cnt
                
        Image.frombytes("RGB", (width, height), bytes(outtmp),"raw", "BGR;16", 0, 1).save(f"{i_path}{tmpnam}.png")
        
    elif widthtype == 0x00 and heighttype == 0x00:
        outtmp = dfxd.read()
        Image.frombytes("RGB", (width, height), outtmp,"raw", "BGR;16", 0, 1).save(f"{i_path}{tmpnam}.png")
    
    fd.seek(icuroffs)
    

