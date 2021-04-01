import utils
import os

sz = os.path.getsize("rel_c")
fd = open("rel_c", "rb")
#fd.seek(0x7a8020)

outp = bytearray()

while fd.tell() < sz:
    #print(fd.tell())
    tt = utils.ioread_u16BitLE(fd)
            
    if tt != 0xad45:
        outp += utils.put_u16BitLE(tt)
    else:
    	d = utils.ioread_u16BitLE(fd)
    	outp += fd.read(2)*d
    
       
    
open("rel_c_out","wb").write(outp)

