import sys
from io import BytesIO, IOBase

def make_key(a):
    buffer = bytearray(b"\0"*len(a))
    offset = 0

    while offset < len(a):        
        needed = min(4,len(a)-offset)
        for e in range(needed):                        
            buffer[offset+e] = a[offset+(needed-(e+1))]            
        offset += needed          
    
    return buffer

def make_key_2(a):
    buffer = bytearray(b"\0"*len(a))
    offset = 0

    while offset < len(a):        
        needed = min(2,len(a)-offset)
        for e in range(needed):                        
            buffer[offset+e] = a[offset+(needed-(e+1))]            
        offset += needed     
    
    return buffer    

def b1tob8(a, skip=0):
    bits = []    

    for b in a:        
        for i in range(8):
            binary = (b >> (7-i)) & 1
            bits.append(binary)
    
    if skip > 0:
        bits = bits[:-skip]

    return bits

def b1tob8_b(a, skip=0):
    bits = []    

    for b in a:        
        for i in range(8):
            binary = (b >> i) & 1
            bits.append(binary)
            
    if skip > 0:            
        bits = bits[:-skip]    

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

def compute_1bpp_size(w,h):
    size = 1
    x = 0
    y = 0
    bits_left = 7

    while True:
        x += 1
        if x >= w:
            y += 1
            x = 0
            if y >= h:
                return size, bits_left

        if bits_left <= 0:
            size += 1
            bits_left = 8

        bits_left -= 1  

def decode(a, w, h, rtype=0, bits=2, alignment=0, last_is_concealed=False, conceal_mode=0, extra_bits=0, edge_mode=0):
    b_io = a
    if not isinstance(a, IOBase):
        b_io = BytesIO(a)

    #p_data = b_io.read(int((w*h)/8))
    key_size, skip_bits = compute_1bpp_size(w,h)   
    #print(key_size, w, h) 

    p_data = b_io.read(key_size)
    if extra_bits > 0:
        p_data += b_io.read(extra_bits)
    elif extra_bits == -1:
        extra_bits_required = 4-(key_size%4)
        if extra_bits_required < 4:
            p_data += b_io.read(extra_bits_required)

    if rtype == 0:
        p_data = make_key(p_data)

    elif rtype == 1 or rtype == 2:
        p_data = make_key_2(p_data)

    pixmap = b1tob8(p_data, skip_bits)
    if rtype == 2:
        pixmap = b1tob8_b(p_data, skip_bits)
    
    b_io.read(alignment)

    output = bytearray()
    state = b""
    width = 0
    height = 0
    last_state = b""
    first_w_pixel_state = b""
    r_data = []

    line = bytearray()

    for t in pixmap:
        if t == 0:
            
            last_state = state

            state = b_io.read(bits)  

            if width <= 0:
                first_w_pixel_state = state
                last_state = state            

            if state == b"":
                state = last_state

            if last_is_concealed and width >= w-1:                     
                output += last_state
                width = -1
            else:
                if (edge_mode == 1 or edge_mode == 2) and width >= w-1:
                    cur_pixel = r_data.pop(0) if height > 0 else first_w_pixel_state if edge_mode == 1 else b""
                    output += cur_pixel+line                
                    r_data.append(state)
                    line = bytearray()
                    width = -1
                    height += 1

                else:
                    if edge_mode == 1 or edge_mode == 2:
                        line += state
                    else:
                        output += state
                    
                
        elif t == 1:
            if state == b"":
                state = b_io.read(bits)

                if state == b"":
                    raise Exception("not enough data")

                if width <= 0:
                    first_w_pixel_state = state
                    last_state = state    

            if (edge_mode == 1 or edge_mode == 2) and width >= w-1:
                cur_pixel = r_data.pop(0) if height > 0 else first_w_pixel_state if edge_mode == 1 else b""
                output += cur_pixel+line                
                r_data.append(state)
                line = bytearray()
                width = -1
                height += 1
                    
            else:
                if edge_mode == 1 or edge_mode == 2:
                    line += state
                else:
                    output += state

            if last_is_concealed and width >= w-1:
                width = -1
                
        width += 1

    if edge_mode == 2:
        output = r_data.pop(0)+output

    #print(len(output))
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