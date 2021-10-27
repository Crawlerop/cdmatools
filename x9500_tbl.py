from x9500_decoder_lib import decode as xdecode
from PIL import Image
from io import BytesIO
import png_chunks
import sys
import struct

if __name__ == "__main__":
    fd = open(sys.argv[1], "rb")    
    
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    fd.seek(int(sys.argv[4], 16))

    for c in range(int(sys.argv[5])):
        offset = struct.unpack("<L", fd.read(4))[0]
        size = struct.unpack("<L", fd.read(4))[0]

        prev_offset = fd.tell()
        fd.seek(offset)

        landscape = fd.read(4) == b"\0\0\0\0"
        dec_data = xdecode(fd.read(size-4), width, height)
        #open("dec_tmp", "wb").write(dec_data)

        dec_i = Image.frombytes("RGB", (height, width) if landscape else (width, height), bytes(dec_data),"raw", "BGR;16", 0, 1 if landscape else -1)
        if landscape:
            dec_i = dec_i.rotate(90, expand=1)

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

        fd.seek(prev_offset)