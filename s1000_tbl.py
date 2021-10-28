from x9500_decoder_lib import decode as xdecode
from PIL import Image
import sys
import struct
import png_chunks
from io import BytesIO

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

def get_trans_value(data, transp):
    offset = 0
    mat = []

    while offset<len(data):
        if data[offset:offset+3] == transp:
            mat.append(0)
        else:
            mat.append(255)

        offset += 3
    
    return mat

if __name__ == "__main__":
    fd = open(sys.argv[1], "rb")        
    
    fd.seek(int(sys.argv[2], 16))

    for c in range(int(sys.argv[3])):
        transparent = False
        transp_pixel = b"\xf8\0\xf8"

        width = fd.read(1)[0]
        if width <= 0: break
        height = fd.read(1)[0]
        if height <= 0: break
        bpp = struct.unpack("<H", fd.read(2))[0]
        if bpp not in [8,16]: break

        offset = struct.unpack("<L", fd.read(4))[0]

        if offset == 0xf81f: # Transparency?
            transparent = True
            offset = struct.unpack("<L", fd.read(4))[0]
            #print(offset)

        palette_offset = struct.unpack("<L", fd.read(4))[0]
        img_type = struct.unpack("<L", fd.read(4))[0]

        prev_offset = fd.tell()
        palette_data = b""

        if bpp == 8:
            fd.seek(palette_offset)
            palette_data = rgb565toi24(fd.read(0x200))
        
        fd.seek(offset)
        
        dec_data = None

        if img_type == 1:
            stride = int(sys.argv[4]) if len(sys.argv) >= 5 else (2 if (width%8) == 0 else 0) if bpp == 8 else 4
            dec_data = xdecode(fd, width, height, 3 if bpp == 8 else 1, int(bpp/8), stride)   
        else:
            dec_data = fd.read((width*height)*int(bpp/8))
                     
        #print(len(dec_data))                     
        #open("dec_tmp", "wb").write(dec_data)

        if bpp == 16:
            dec_i = Image.frombytes("RGB", (width, height), bytes(dec_data),"raw", "BGR;16", 0, 1)
            i_buffer = BytesIO()
            buffer = BytesIO(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
            buffer.seek(8)

            dec_i.save(i_buffer, format="png")
            i_buffer.seek(8)

            while True:
                c_name, c_data = png_chunks.read_png_packet(i_buffer)

                if c_name == "IDAT":                    
                    buffer.write(png_chunks.write_itxt_packet("Decoder", "cdmatools - designed for ROMPhonix server (https://discord.gg/2GKuJjQagp)"))

                buffer.write(png_chunks.write_png_packet(c_name, c_data))
                                
                if c_name == "IEND":
                    break

            while True:
                try:
                    open(f"IMG_{offset}_{c+1}.png", "wb").write(buffer.getvalue())
                    break
                except OSError as e:
                    if e.errno != 22:
                        raise
        elif bpp == 8:
            dec_i = Image.frombytes("P", (width, height), bytes(dec_data))
            dec_i.putpalette(palette_data)
            i_buffer = BytesIO()
            buffer = BytesIO(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A")
            buffer.seek(8)

            dec_i.save(i_buffer, format="png")
            i_buffer.seek(8)

            while True:
                c_name, c_data = png_chunks.read_png_packet(i_buffer)
                buffer.write(png_chunks.write_png_packet(c_name, c_data))
                
                if c_name == "PLTE":
                    if transparent:
                        buffer.write(png_chunks.write_png_packet("tRNS", bytes(get_trans_value(palette_data, transp_pixel))))
                    buffer.write(png_chunks.write_itxt_packet("Decoder", "cdmatools - designed for ROMPhonix server (https://discord.gg/2GKuJjQagp)"))

                if c_name == "IEND":
                    break

            while True:
                try:
                    open(f"IMG_{offset}_{c+1}.png", "wb").write(buffer.getvalue())
                    break
                except OSError as e:
                    if e.errno != 22:
                        raise

        fd.seek(prev_offset)