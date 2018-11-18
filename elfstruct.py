from elftypes import *
from collections import OrderedDict
from elfdicts import *

class elfstruct:
    def __init__(self, file):
        self.f = file
        self.check_binary()
        self.Ehdr = []
        self.Ehdr_d = OrderedDict()
        self.Phdr = []
        self.Phdr_d = OrderedDict()
        self.Shdr = []
        self.Shdr_d = OrderedDict()

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
        self.Ehdr.append(self.f.read(4)) # magic
        self.Ehdr.append(self.f.read(1)) # class
        self.Ehdr.append(self.f.read(1)) # data
        self.Ehdr.append(self.f.read(1)) # version
        self.Ehdr.append(self.f.read(1)) # osabi
        self.Ehdr.append(self.f.read(1)) # abiversion
        self.Ehdr.append(self.f.read(7)) # padding
        self.Ehdr.append(self.f.read(2)) # type
        self.Ehdr.append(self.f.read(2)) # machine
        self.Ehdr.append(self.f.read(4)) # version
        self.Ehdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
        self.Ehdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
        self.Ehdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
        self.Ehdr.append(self.f.read(4)) # flags
        self.Ehdr.append(self.f.read(2)) # ehsize
        self.Ehdr.append(self.f.read(2)) # phentsize
        self.Ehdr.append(self.f.read(2)) # phnum
        self.Ehdr.append(self.f.read(2)) # shentsize
        self.Ehdr.append(self.f.read(2)) # shnum
        self.Ehdr.append(self.f.read(2)) # shstrndx
        self.Ehdr = list(map(lambda f: toInt(f, self.little_endian), self.Ehdr))
        combined = OrderedDict(zip(Ehdr_names, self.Ehdr))
        return combined


    def Elf_Phdr(self):
        self.f.seek(self.Ehdr[11]) # phoff
        # reading the data
        for i in range(self.Ehdr[16]):
            self.Phdr.append(self.f.read(4))
            self.Phdr.append(self.f.read(4) if self.arch == 64 else self.f.read(0))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(0) if self.arch == 64 else self.f.read(4))
            self.Phdr.append(self.f.read(8) if self.arch == 64 else self.f.read(4))
            self.Phdr = list(map(lambda f: toInt(f, self.little_endian), self.Phdr))
            combined = OrderedDict(zip(Phdr64_names if self.arch == 64 else Phdr32_names, self.Phdr))
            self.Phdr_d[i] = combined
            self.Phdr.clear()
        return self.Phdr_d

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
            self.Shdr[i] = self.f.read(size)
        return self.Shdr

if __name__ == '__main__':
    x = elfstruct(open('server', 'r+b'))
    x.Elf_Ehdr()
    lol = x.Elf_Phdr()
    #x.Elf_Shdr()
