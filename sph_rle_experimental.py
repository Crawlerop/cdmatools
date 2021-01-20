import struct
import os
import sys

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

out = open(sys.argv[2], "wb")
obuf = bytearray()

while fd.tell() < sz:
	rl_offs = struct.unpack("<H", fd.read(2))[0]
	if rl_offs == 1:
		bit = fd.read(2)
		cnt = struct.unpack("<H", fd.read(2))[0]
		obuf += bit*cnt
	else:
		obuf += struct.pack("<H", rl_offs)
		
out.write(obuf)
		
