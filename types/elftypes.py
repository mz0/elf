import struct

""" unsigned little_endian 8-bit int """
def Elf_ULInt8(value):
    return struct.pack('<B', value)

""" unsigned little_endian 16-bit int """
def Elf_ULInt16(value):
    return struct.pack('<H', value)

""" unsigned little_endian 32-bit int """
def Elf_ULInt32(value):
    return struct.pack('<L', value)

""" unsigned little_endian 64-bit int """
def Elf_ULInt64(value):
    return struct.pack('<Q', value)

""" unsigned big_endian 8-bit int """
def Elf_UBInt8(value):
    return struct.pack('>B', value)

""" unsigned big_endian 16-bit int """
def Elf_UBInt16(value):
    return struct.pack('>H', value)

""" unsigned big_endian 32-bit int """
def Elf_UBInt32(value):
    return struct.pack('>L', value)

""" unsigned big_endian 64-bit int """
def Elf_UBInt64(value):
    return struct.pack('>Q', value)
