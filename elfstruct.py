from elftypes import *
from collections import OrderedDict

class elfstruct:
    def __init__(self, file):
        # assert Architecture == 64 or Architecture == 32
        # self.arch = Architecture
        self.f = file
        self.check_binary()
        self.Phdr = OrderedDict()
        self.Shdr = OrderedDict()

    def check_binary(self):
        magic = self.f.read(0x06)
        if magic[:0x04] != b'\x7F\x45\x4c\x46':
            raise ValueError('Corrupted magic:', magic[:0x04])

        if magic[0x04] == 1:
            self.arch = 32
        elif magic[0x04] == 2:
            self.arch = 64
        else:
            raise ValueError('Unknown Architecture')

        if magic[0x05] == 1:
            self.little_endian = True
        elif magic[0x05] == 2:
            self.little_endian = False
        else:
            raise ValueError('Unknown endianness')

    def Elf_Ehdr(self):
        self.f.seek(0, 0)
        return self.f.read(0x3E) if self.arch == 64 else self.f.read(0x32)

    def Elf_Phdr(self):
        # getting program header offset, count and size
        if self.arch == 64:
            self.f.seek(0x20, 0)
            phoff = toInt(self.f.read(8), self.little_endian)
            self.f.seek(0x36, 0)
            size = toInt(self.f.read(2), self.little_endian)
            count = toInt(self.f.read(2), self.little_endian)
        else:
            self.f.seek(0x1C, 0)
            phoff = toInt(self.f.read(4), self.little_endian)
            self.f.seek(0x2A, 0)
            size = toInt(self.f.read(2), self.little_endian)
            count = toInt(self.f.read(2), self.little_endian)

        # moving to phoff address
        self.f.seek(phoff)
        # reading the data
        for i in range(count):
            self.Phdr[str(i)] = self.f.read(size)
        return self.Phdr

    def Elf_Shdr(self):
        # getting section header offset, name index, count and size
        if self.arch == 64:
            self.f.seek(0)
            self.f.seek(0x28)
            shoff = toInt(self.f.read(8), self.little_endian)
            self.f.seek(0x3A)
            size = toInt(self.f.read(2), self.little_endian)
            count = toInt(self.f.read(2), self.little_endian)
            strndx = toInt(self.f.read(2), self.little_endian)
        else:
            self.f.seek(0)
            self.f.seek(0x20)
            shoff = toInt(self.f.read(4), self.little_endian)
            self.f.seek(0x2E)
            size = toInt(self.f.read(2), self.little_endian)
            count = toInt(self.f.read(2), self.little_endian)
            strndx = toInt(self.f.read(2), self.little_endian)

        # moving to shoff address
        self.f.seek(shoff)
        # reading the data
        for i in range(count):
            self.Shdr[str(i)] = self.f.read(size)
        return self.Shdr

if __name__ == '__main__':
    x = elfstruct(open('server1', 'rb'))
    print(x.Elf_Ehdr())
    x.Elf_Phdr()
    x.Elf_Shdr()
