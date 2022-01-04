import struct
import os
import sys
from io import BytesIO

file_size = os.path.getsize(sys.argv[1])
file_data = open(sys.argv[1], "rb")

output = open(sys.argv[2], "wb")
output_buffer = bytearray()

decoding_buffer = BytesIO()

delimiter = file_data.read(2)

while file_data.tell() < file_size:
    rle_bit = file_data.read(2)
    if rle_bit == delimiter:
        count, offset = struct.unpack("<HH", file_data.read(4))
        previous_offset = decoding_buffer.tell()
        decoding_buffer.seek(offset*2)
        copied_pixels = decoding_buffer.read(2*count)
        decoding_buffer.seek(previous_offset)  
        decoding_buffer.write(copied_pixels)
        output_buffer += copied_pixels
		
    else:        
        decoding_buffer.write(rle_bit)
        output_buffer += rle_bit

output.write(output_buffer)
		
