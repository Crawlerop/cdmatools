import zlib
import typing
import struct
import io

def write_png_packet(chunk: str,data: typing.Union[bytes,bytearray]):
    return struct.pack(">L", len(data))+chunk.encode("ascii")+data+struct.pack(">L", zlib.crc32(chunk.encode("ascii")+data))
    
def write_itxt_packet(cat: str, text: str):
    return write_png_packet("iTXt", cat.encode("ascii")+b"\0\0\0\0\0"+text.encode("ascii"))

def read_png_packet(fd: io.IOBase):
    chunk_size = struct.unpack(">L", fd.read(4))[0]
    chunk_name = fd.read(4).decode("ascii")
    chunk_data = fd.read(chunk_size)    
    assert struct.unpack(">L", fd.read(4))[0] == zlib.crc32(chunk_name.encode("ascii")+chunk_data)
    return (chunk_name, chunk_data)