import struct
import os
import sys

if len(sys.argv) < 3:
	print(f"Not enough arguments! usage: {sys.argv[0]} file output [skip_bit_offsets]", file=sys.stderr)
	sys.exit(1)

skip_bits = []
if len(sys.argv) > 3:
	skip_bits = [int(k, 16) for k in sys.argv[3].split(",")]

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

out = open(sys.argv[2], "wb")
obuf = bytearray()

while fd.tell() < sz:
	rl_offs = struct.unpack("<H", fd.read(2))[0]
	if rl_offs == 1 and fd.tell()-2 not in skip_bits:
		bit = fd.read(2)
		cnt = struct.unpack("<H", fd.read(2))[0]
		obuf += bit*cnt
	else:
		obuf += struct.pack("<H", rl_offs)
		
out.write(obuf)
		
