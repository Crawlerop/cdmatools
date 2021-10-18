import os
import struct
import sys

if __name__ == "__main__":
    fd_data = open(sys.argv[1], "rb")
    fd_size = os.path.getsize(sys.argv[1])

    efs_files = {}
    efs_block_arrangements = {}    

    while fd_data.tell()<fd_size:
        efs_full = False

        efs_type = struct.unpack("<H", fd_data.read(2))[0]
        if efs_type == 0xffff or efs_type == 0x0:
            continue
        efs_id = struct.unpack("<H", fd_data.read(2))[0]
        efs_block_id = struct.unpack("<H", fd_data.read(2))[0]
        efs_data_type = struct.unpack("<H", fd_data.read(2))[0]
        efs_block_type = struct.unpack("<H", fd_data.read(2))[0]
        efs_block_size = struct.unpack("<H", fd_data.read(2))[0]
        name_length = -1        

        #print(efs_type)
        if efs_type == 0xfe:
            e_data = fd_data.read(efs_block_size)
            if efs_id in efs_files:                
                #efs_files[efs_id]["data"][efs_block_id] = e_data
                if efs_data_type != 0x1 or efs_block_id not in efs_files[efs_id]["data"]: efs_files[efs_id]["data"][efs_block_id] =  e_data
                if efs_block_id not in efs_block_arrangements[efs_id]: efs_block_arrangements[efs_id].append(efs_block_id)           
            else:
                efs_files[efs_id] = {"data": {}, "file_name": ""}
                efs_block_arrangements[efs_id] = []
                #efs_files[efs_id]["data"][efs_block_id] = e_data
                if efs_data_type != 0x1 or efs_block_id not in efs_files[efs_id]["data"]: efs_files[efs_id]["data"][efs_block_id] = e_data
                if efs_block_id not in efs_block_arrangements[efs_id]: efs_block_arrangements[efs_id].append(efs_block_id)  
   

        elif efs_type == 0xed or efs_type == 0x6c or efs_type == 0xdb or efs_type == 0xfb or efs_type == 0x6d or efs_type == 0x5b:                        
            if efs_data_type != 0x1:
                if not efs_id in efs_files: efs_files[efs_id] = {"data": {}, "file_name": ""}
                if not efs_id in efs_block_arrangements: efs_block_arrangements[efs_id] = []                
                fd_data.read(0x10)
                name_length = fd_data.read(1)[0]           
                efs_filename_b = fd_data.read(name_length)
                efs_filename = efs_filename_b[:-1].decode("ascii")     
                #print(efs_filename)                              
                if efs_data_type != 0x1: efs_files[efs_id]["data"][efs_block_id] = fd_data.read(efs_block_size)  
                if efs_data_type != 0x1 and efs_block_id not in efs_block_arrangements[efs_id]: efs_block_arrangements[efs_id].append(efs_block_id)
                efs_files[efs_id]["file_name"] = efs_filename
            else:
                efs_full = True
                fd_data.read(efs_block_size)
       
        else:
            raise Exception(efs_type, fd_data.tell())

        padding = 0xf0-efs_block_size        
        if efs_type != 0xfe and not efs_full:
            padding = (0xf0-(0x11+name_length))-efs_block_size

        if padding > 0: fd_data.read(padding)    
        fd_data.read(4)    
    
    output_folder = f"{sys.argv[1]}_ext/"
    os.makedirs(output_folder, exist_ok=True)

    for k in efs_block_arrangements:        
        if not efs_files[k]['file_name']: efs_files[k]['file_name'] = f"UNKNOWN_{k}"
        os.makedirs(f"{output_folder}{os.path.split(efs_files[k]['file_name'])[0]}", exist_ok=True)        
        out_file = open(f"{output_folder}{efs_files[k]['file_name']}", "wb")  

        data = []  
        for index in sorted(efs_block_arrangements[k]):       
            data.append(efs_files[k]["data"][index])
        out_file.write(b"".join(data))
    
    #print(efs_files[255]["data"])
    #print(sorted(efs_block_arrangements[255]))

          
        