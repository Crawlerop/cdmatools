import sys
from io import BytesIO, IOBase

def make_key(a):
    buffer = bytearray(b"\0"*len(a))
    offset = 0

    while offset < len(a):           
        buffer[offset] = a[offset+3]
        buffer[offset+1] = a[offset+2]
        buffer[offset+2] = a[offset+1]
        buffer[offset+3] = a[offset]        
        offset += 4
    
    return buffer

def make_key_2(a):
    buffer = bytearray(b"\0"*len(a))
    offset = 0

    while offset < len(a):           
        buffer[offset] = a[offset+1]
        buffer[offset+1] = a[offset]      
        offset += 2
    
    return buffer    

def b1tob8(a):
    bits = []    

    for b in a:        
        for i in range(8):
            binary = (b >> (7-i)) & 1
            bits.append(binary)
    
    return bits

def b1tob8_b(a):
    bits = []    

    for b in a:        
        for i in range(8):
            binary = (b >> i) & 1
            bits.append(binary)
    
    return bits

'''
def make_rle_table(b):
    tbl = []
    count = 0

    for bit in b1tob8(make_key(b)):
        if bit == 0:
            if count > 0:
                tbl.append(count)
            count = 1
        else:
            count += 1

    return tbl
'''

def decode(a, w, h, rtype=0, bits=2, alignment=0, last_is_concealed=False, conceal_mode=0):
    b_io = a
    if not isinstance(a, IOBase):
        b_io = BytesIO(a)

    p_data = b_io.read(int((w*h)/8))

    if rtype == 0:
        p_data = make_key(p_data)

    elif rtype == 1 or rtype == 2:
        p_data = make_key_2(p_data)

    pixmap = b1tob8(p_data)
    if rtype == 2:
        pixmap = b1tob8_b(p_data)

    b_io.read(alignment)

    output = bytearray()
    state = b""
    width = 0
    last_state = b""

    for t in pixmap:
        if t == 0:
            if conceal_mode == 0:
                last_state = state

            state = b_io.read(bits)    

            if conceal_mode == 1 and width <= 0:
                last_state = state            

            if state == b"":
                raise Exception("not enough data")
            if last_is_concealed and width >= w-1:                     
                output += last_state
                width = -1
            else:
                output += state
                
        elif t == 1:
            output += state
            if last_is_concealed and width >= w-1:
                width = -1
                
        width += 1

    return output

'''''
if __name__ == "__main__":    
    fd = open(sys.argv[1], "rb")    
    w, h = int(sys.argv[2]), int(sys.argv[3])
    out = bytearray()
    flag = fd.read(4)

     flag in [b"\1\0\0\0", b"\0\0\0\0"]:
        key = b1tob8(make_key(fd.read(int((w*h)/8))))
        
        state = b""
        output = bytearray()

        for p in key:
            if p == 0:
                state = fd.read(2)
                output += state
            elif p == 1:
                output += state
                            
        
        offset = ((w*h)*2)-(w*2)

        width_c = 0
        height_c = h-1

        for p in key:
            if height_c <= 0:
                break

            if p == 0:
                state = fd.read(2)
                output[offset:offset+2] = state            
            elif p == 1:
                output[offset:offset+2] = state

            offset += 2
            width_c += 1

            if width_c >= w:
                height_c -= 1
                width_c = 0
                offset -= w*4


        out += output
        if input("Skip? ") == "y":
            fd.read(2)

        flag = fd.read(4)

    open("img_test_b.bin", "wb").write(out)
'''