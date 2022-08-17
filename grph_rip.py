import struct
import sys
import io
from PIL import Image
import zlib

if __name__ == "__main__":
    fd = open(sys.argv[1], "rb")    

    assert fd.read(4) == b"GRPH"
    fd.read(8) 
    count = struct.unpack("<L", fd.read(4))[0]

    for cnt in range(count):
        offset, size = struct.unpack("<LL", fd.read(8))    
        if offset <= 0 or size <= 0: continue

        temp_offset = fd.tell()
        fd.seek(offset)
        data_temp = io.BytesIO(fd.read(size))
        height, width, bpp, comptype, anim, anim2 = struct.unpack("<HHHHHH", data_temp.read(0xc))

        '''
        if bpp == 1:
            wp = (8 - (width % 8))
            width = width + (0 if wp == 8 else wp)
            hp = (8 - (height % 8))
            height = height + (0 if hp == 8 else hp) 

            print(width, height)
        '''

        #print(width, height, bpp, comptype, anim, anim2, hex(offset))        

        assert bpp in [16,1]

        if comptype & 1:
            data = zlib.decompress(data_temp.read())                  
        else:
            data = data_temp.read()
        #else:
        #    raise Exception(comptype)  

        if bpp == 16:
            nframes = len(data) // (width*height*2)
        elif bpp == 1:            
            nframes = len(data) // ((width*height) // 8)
            print(nframes, hex((width*height) // 8), width, height, hex(len(data)))

        data = io.BytesIO(data)
        #print(nframes)

        for n in range(nframes):
            if bpp == 16:
                Image.frombytes("RGB", (width, height), bytes(data.read(width*height*2)),"raw", "BGR;16", 0, 1).save(f"IMG_{cnt:03d}_{width}_{height}_{bpp}_{n}.png")
            elif bpp == 1:                
                Image.frombytes("1", (width, height), bytes(data.read((width*height) // 4))).save(f"IMG_{cnt:03d}_{width}_{height}_{bpp}_{n}.png")

        #open(f"IMG_{cnt:03d}_{width}_{height}_{bpp}.bin", "wb").write(data)
        fd.seek(temp_offset)

        
