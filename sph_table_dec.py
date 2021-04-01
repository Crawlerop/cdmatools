import struct
import os
import sys
from io import BytesIO

if len(sys.argv) < 5:
	print(f"Not enough arguments! usage: {sys.argv[0]} file table_offset count output", file=sys.stderr)
	sys.exit(1)

fd = open(sys.argv[1], "rb")
fd.seek(int(sys.argv[2], 16))

out = open(sys.argv[4], "wb")

for i in range(int(sys.argv[3])):
	print(i);
	offs = struct.unpack("<L", fd.read(4))[0]
	ofsz = struct.unpack("<L", fd.read(4))[0]
	ofs_orig = fd.tell()
	fd.seek(offs)
	b_data = BytesIO(fd.read(ofsz))
	obuf = bytearray()

	try: 
		while b_data.tell() < ofsz:
			p = b_data.read(2)
			if p == b"\1\0":
				bit = b_data.read(2)
				if bit == b"\1\0":
					obuf += p
				else:
					cnt = struct.unpack("<H", b_data.read(2))[0]
					obuf += bit*cnt
			else:
				obuf += p
	except Exception:
		pass
			
	out.write(obuf)
	fd.seek(ofs_orig)
	

		
