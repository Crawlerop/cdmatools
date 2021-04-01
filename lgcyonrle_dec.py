import struct
import os
import sys

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")
#fd.seek(0x7a8020)

outp = bytearray()

while fd.tell() < sz:
    #print(fd.tell())
    tt = struct.unpack("<H", fd.read(2))[0]
            
    if tt != 0xad45:
        outp += struct.pack("<H", tt)
    else:
    	d = struct.unpack("<H", fd.read(2))[0]
    	outp += fd.read(2)*d
    
       
    
open(sys.argv[2],"wb").write(outp)

