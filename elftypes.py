import struct

def toInt(value, order):
    return int.from_bytes(value, byteorder='little' if order else 'big')


""" unsigned little_endian 8-bit int """
def ULInt8(value):
    return struct.pack('<B', value)

""" unsigned little_endian 16-bit int """
def ULInt16(value):
    return struct.pack('<H', int.from_bytes(value, byteorder='little'))

""" unsigned little_endian 32-bit int """
def ULInt32(value):
    return struct.pack('<L', int.from_bytes(value, byteorder='little'))

""" unsigned little_endian 64-bit int """
def ULInt64(value):
    return struct.pack('<Q', int.from_bytes(value, byteorder='little'))

""" unsigned big_endian 8-bit int """
def UBInt8(value):
    return struct.pack('>B', value)

""" unsigned big_endian 16-bit int """
def UBInt16(value):
    return struct.pack('>H', int.from_bytes(value, byteorder='big'))

""" unsigned big_endian 32-bit int """
def UBInt32(value):
    return struct.pack('>L', int.from_bytes(value, byteorder='big'))

""" unsigned big_endian 64-bit int """
def UBInt64(value):
    return struct.pack('>Q', int.from_bytes(value, byteorder='big'))
