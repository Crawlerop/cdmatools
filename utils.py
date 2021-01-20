import numpy as np

def read_64BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+8)], dtype=np.int64)[0]

def read_64BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+8)], dtype=np.int64).byteswap()[0]

def ioread_64BitLE(fd):
    return np.frombuffer(fd.read(8), dtype=np.int64)[0]

def ioread_64BitBE(fd):
    return np.frombuffer(fd.read(8), dtype=np.int64).byteswap()[0]

def put_64BitLE(num):
    return np.int64(num).tobytes()

def put_64BitBE(num):
    return np.int64(num).byteswap().tobytes()

def read_u64BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+8)], dtype=np.uint64)[0]

def read_u64BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+8)], dtype=np.uint64).byteswap()[0]

def ioread_u64BitLE(fd):
    return np.frombuffer(fd.read(8), dtype=np.uint64)[0]

def ioread_u64BitBE(fd):
    return np.frombuffer(fd.read(8), dtype=np.uint64).byteswap()[0]

def put_u64BitLE(num):
    return np.uint64(num).tobytes()

def put_u64BitBE(num):
    return np.uint64(num).byteswap().tobytes()

def read_32BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+4)], dtype=np.int32)[0]

def read_32BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+4)], dtype=np.int32).byteswap()[0]

def ioread_32BitLE(fd):
    return np.frombuffer(fd.read(4), dtype=np.int32)[0]

def ioread_32BitBE(fd):
    return np.frombuffer(fd.read(4), dtype=np.int32).byteswap()[0]

def put_32BitLE(num):
    return np.int32(num).tobytes()

def put_32BitBE(num):
    return np.int32(num).byteswap().tobytes()

def read_u32BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+4)], dtype=np.uint32)[0]

def read_u32BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+4)], dtype=np.uint32).byteswap()[0]

def ioread_u32BitLE(fd):
    return np.frombuffer(fd.read(4), dtype=np.uint32)[0]

def ioread_u32BitBE(fd):
    return np.frombuffer(fd.read(4), dtype=np.uint32).byteswap()[0]

def put_u32BitLE(num):
    return np.uint32(num).tobytes()

def put_u32BitBE(num):
    return np.uint32(num).byteswap().tobytes()

def read_16BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+2)], dtype=np.int16)[0]

def read_16BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+2)], dtype=np.int16).byteswap()[0]

def ioread_16BitLE(fd):
    return np.frombuffer(fd.read(2), dtype=np.int16)[0]

def ioread_16BitBE(fd):
    return np.frombuffer(fd.read(2), dtype=np.int16).byteswap()[0]

def put_16BitLE(num):
    return np.int16(num).tobytes()

def put_16BitBE(num):
    return np.int16(num).byteswap().tobytes()

def read_u16BitLE(data, offset):
    return np.frombuffer(data[offset:(offset+2)], dtype=np.uint16)[0]

def read_u16BitBE(data, offset):
    return np.frombuffer(data[offset:(offset+2)], dtype=np.uint16).byteswap()[0]

def ioread_u16BitLE(fd):
    return np.frombuffer(fd.read(2), dtype=np.uint16)[0]

def ioread_u16BitBE(fd):
    return np.frombuffer(fd.read(2), dtype=np.uint16).byteswap()[0]

def put_u16BitLE(num):
    return np.uint16(num).tobytes()

def put_u16BitBE(num):
    return np.uint16(num).byteswap().tobytes()

def read_8Bit(data, offset):
    return np.frombuffer(data[offset:(offset+1)], dtype=np.int8)[0]

def ioread_8Bit(fd):
    return np.frombuffer(fd.read(1), dtype=np.int8).byteswap()[0]

def put_8Bit(num):
    return np.int8(num).tobytes()

def read_u8Bit(data, offset):
    return np.frombuffer(data[offset:(offset+1)], dtype=np.uint8)[0]

def ioread_u8Bit(fd):
    return np.frombuffer(fd.read(1), dtype=np.uint8).byteswap()[0]

def put_u8Bit(num):
    return np.uint8(num).tobytes()

def read_4Bit(data, offset):
    nibble = offset & 1
    datoffset = int(offset / 2)
    if nibble:
        cur = data[datoffset] & 0xf
        if cur > 7:
            cur -= 16
        return cur
    else:
        cur = data[datoffset] >> 4
        if cur > 7:
            cur -= 16
        return cur

def ioread_4Bit(fd):
    data = fd.read(1)
    return read_4Bit(data, 0), read_4Bit(data, 1)

def read_u4Bit(data, offset):
    nibble = offset & 1
    datoffset = int(offset / 2)
    if nibble:
        return data[datoffset] & 0xf
    else:
        return data[datoffset] >> 4

def ioread_u4Bit(fd):
    data = fd.read(1)
    return read_u4Bit(data, 0), read_u4Bit(data, 1)

def deinterleave(data, blocks=1024, splits=2):
    offset = 0
    channel = 0
    blockout = []
    for _ in range(splits):
        blockout.append(bytearray())

    while offset<len(data):
        bs = blocks
        if (offset+blocks) > len(data):
            bs = (offset+blocks)-len(data)

        blockout[channel] += (data[offset:offset+bs])

        offset += bs
        channel += 1

        if channel >= splits:
            channel = 0

    return blockout

def longestBytesArray(datas):
    longest = 0
    longindex = 0
    index = 0
    while index<len(datas):
        if len(datas[index]) > longest:
            longest = len(datas[index])
            longindex = index
        index += 1
    return datas[longindex]

def interleave(datas, blocks=1024):
    offset = 0
    channel = 0
    size = len(longestBytesArray(datas))
    outp = bytearray()
    while offset<size:
        bs = blocks
        if (offset+blocks) > size:
            bs = (offset+blocks)-size

        ret = datas[channel][offset:offset+bs]
        if len(ret) < bs: # Truncated length?
            outp += ret
            for _ in range(bs-len(ret)):
                outp += b"\x00" # Fill with padding-zeroes
        else:
            outp += ret

        channel += 1

        if channel >= len(datas):
            channel = 0
            offset += bs

    return outp

def deblock(data, blocks=2048, headers=32):
    offset = 0
    done = 0
    output = {"blocks":[],"headers":[]}

    data = bytearray(data)

    while True:
        if done <= 0:
            ret = data[offset:(offset+blocks)]
            if len(ret) <= 0:
                done += 1
            else:
                output["blocks"].append(ret)
            #print("a:",ret)
            offset += blocks
        if done <= 1:
            ret = data[offset:(offset+headers)]
            if len(ret) <= 0:
                done += 1
            else:
                output["headers"].append(ret)
            #print("b:",ret)
            offset += headers
        if done >= 2:
            break
    return output

def rle(bits, rlen=4, limit=1024):
    lastbits = bytearray()
    rlelength = 0
    rlstep = -1
    offset = 0
    out = {"bits": [], "table": []}
    while offset<len(bits):
        curbit = bytearray(bits[offset:(offset+rlen)])
        if curbit != lastbits or rlelength >= limit:
            rlelength = 0
            out["bits"].append(curbit)
            out["table"].append(0)
            rlstep += 1
            lastbits = curbit
        rlelength += 1
        out["table"][rlstep] += 1
        offset += rlen
    return out
    
def derle(bits, table):
    if not isinstance(bits, list):
        raise TypeError("derle only accept list as bytes")
    if not isinstance(table, list):
        raise TypeError("derle only accept list as tables")
    if len(bits) != len(table):
        raise ValueError("Table length is not same as the data one.")
    outp = bytearray()
    offset = 0
    for bit in bits:
        for _ in range(table[offset]):
            outp += bit
        offset += 1
    return outp

if __name__ == "__main__":
    print(interleave([b"\x01\x02\x03\x04\xba",b"\x05\x06\x07"], 2))
    print(deinterleave(interleave([b"\x01\x02\x03\x04\xba",b"\x05\x06\x07"], 2), 2))
    print(deblock(b"ABCDEFGH-BLK-IJKLMNOP-BLK-QRSTUVWX", 8, 5))
    print(rle(b"AAAAAAAABBBB", 5))
    print(rle(b"AA"*510, 2))
    print(derle([b'AA', b'AA'], [255,255]))
