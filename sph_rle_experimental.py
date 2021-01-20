import utils
import os
import sys

sz = os.path.getsize(sys.argv[1])
fd = open(sys.argv[1], "rb")

out = open(sys.argv[2], "wb")
obuf = bytearray()

while fd.tell() < sz:
	rl_offs = utils.ioread_u16BitLE(fd)
	if rl_offs == 1:
		bit = fd.read(2)
		cnt = utils.ioread_u16BitLE(fd)
		obuf += bit*cnt
	else:
		obuf += utils.put_u16BitLE(rl_offs)
		
out.write(obuf)
		
