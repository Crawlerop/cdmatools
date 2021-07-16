import os
import sys
import struct
import zlib

def main():
	if len(sys.argv) < 2:
		print("Not enough arguments")
		sys.exit(1)
	f = bytearray()
	i = open(sys.argv[1], "rb")
	g = i.read()
	while g != b"":
		f += g
		g = i.read()
	offset = f.find(struct.pack("<HH", int(sys.argv[3]), int(sys.argv[2])))
	if not os.path.exists(sys.argv[1] + "_ext_anm"): os.mkdir(sys.argv[1] + "_ext_anm")	
	c = 0	
	while offset != -1:
		if f[offset+0xc] != 0x78:
			offset = offset = f.find(struct.pack("<HH", int(sys.argv[3]), int(sys.argv[2])), offset+1)
			continue		
		c += 1
		try:
			lf = zlib.decompress(f[offset+0xc:])
			open(f"{sys.argv[1]}_ext_anm/ANM_{sys.argv[2]}_{sys.argv[3]}_{c}.ani", "wb").write(lf)
		except Exception:
			c -= 1
			pass
		offset += 1
		offset = f.find(struct.pack("<HH", int(sys.argv[3]), int(sys.argv[2])), offset)

if __name__ == "__main__":
	main()
