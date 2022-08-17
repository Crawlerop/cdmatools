import struct
import sys
import io
from PIL import Image
import zlib

def bpp2tobpp8(data):
    maps = [0x00, 0x40, 0x80, 0xff]
    offset = 0
    out_temp = bytearray()
    while offset<len(data):
        out_temp.append(maps[(data[offset] >> 6) & 3])
        out_temp.append(maps[(data[offset] >> 4) & 3])
        out_temp.append(maps[(data[offset] >> 2) & 3])
        out_temp.append(maps[data[offset] & 3])

        offset += 1
    return bytes(out_temp)

if __name__ == "__main__":
    fd = open(sys.argv[1], "rb")    

    assert fd.read(4) == b"GRPH"
    fd.read(8) 
    count = struct.unpack("<L", fd.read(4))[0]

    for cnt in range(count):
        offset, size = struct.unpack("<LL", fd.read(8))    
        if offset <= 0 or size <= 0 or offset >= 0xffffffff or size >= 0xffffffff: continue

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

        if bpp == 2:
            wp = (4 - (width % 4))
            width_p = width + (0 if wp == 4 else wp)
        elif bpp == 1:
            wp = (8 - (width % 8))
            width_p = width + (0 if wp == 8 else wp)

        #print(width, height, bpp, comptype, anim, anim2, hex(offset))        

        assert bpp in [16,2,1]

        #add_2 = (comptype >> 5) & 1
        is_ifeg = (comptype >> 4) & 1

        if not is_ifeg:
            if comptype & 1:
                data = zlib.decompress(data_temp.read())                  
            else:
                data = data_temp.read()
        else:
            data = data_temp.read()
        #else:
        #    raise Exception(comptype)  

        if not is_ifeg:
            if bpp == 16:
                nframes = len(data) // (width*height*2)
            elif bpp == 2:                
                #nframes = len(data) // round((width*height) / 4)
                nframes = len(data) // ((width_p*height) // 4)
                print(nframes, hex(offset))
            elif bpp == 1:            
                nframes = len(data) // ((width_p*height) // 8)
                #print(nframes, hex((width*height) // 8), width, height, hex(len(data)))

            data = io.BytesIO(data)
            #print(nframes)

            for n in range(nframes):
                if bpp == 16:
                    Image.frombytes("RGB", (width, height), bytes(data.read(width*height*2)),"raw", "BGR;16", 0, 1).save(f"IMG_{cnt:03d}_{width}_{height}_{bpp}_{n}.png")
                elif bpp == 2:                                    
                    converted = bpp2tobpp8(data.read(((width_p*height) // 4)))
                    print(len(converted), width, height, width_p)
                    Image.frombytes("L", (width, height), converted).save(f"IMG_{cnt:03d}_{width}_{height}_{bpp}_{n}.png")
                elif bpp == 1:                
                    Image.frombytes("1", (width, height), bytes(data.read((width*height) // 8))).save(f"IMG_{cnt:03d}_{width}_{height}_{bpp}_{n}.png")
        else:
            open(f"IMG_{cnt:03d}_{width}_{height}_{bpp}.ani", "wb").write(data)

        #open(f"IMG_{cnt:03d}_{width}_{height}_{bpp}.bin", "wb").write(data)
        fd.seek(temp_offset)

        
