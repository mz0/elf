from elftypes import *
from collections import OrderedDict
from elfdicts import *

class elfstruct:
    def __init__(self, file):
        self.f = file
        self.check_binary()
        self.Ehdr = []
        self.Phdr, self.Phdr_d = [], OrderedDict()
        self.Shdr, self.Shdr_d = [], OrderedDict()
        self.Elf_Ehdr()

    def check_binary(self):
        magic = self.f.read(0x06)
        if magic[:0x04] != b'\x7F\x45\x4c\x46':
            raise ValueError('Corrupted magic:', magic[:0x04])

        if magic[0x04] == 1:
            self.arch = False
        elif magic[0x04] == 2:
            self.arch = True
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
        if self.arch:
            [self.Ehdr.append(self.f.read(i)) for i in Ehdr64]
        else:
            [self.Ehdr.append(self.f.read(i)) for i in Ehdr32]
        self.Ehdr = list(map(lambda f: toInt(f, self.little_endian), self.Ehdr))
        self.Ehdr_d = OrderedDict(zip(Ehdr_names, self.Ehdr))
        return self.Ehdr_d


    def Elf_Phdr(self):
        self.f.seek(self.Ehdr[11])
        for i in range(self.Ehdr[16]):
            if self.arch:
                [self.Phdr.append(self.f.read(i)) for i in Phdr64]
            else:
                [self.Phdr.append(self.f.read(i)) for i in Phdr32]
            self.Phdr = list(map(lambda f: toInt(f, self.little_endian), self.Phdr))
            combined = OrderedDict(zip(Phdr64_names if self.arch else Phdr32_names, self.Phdr))
            self.Phdr_d[i] = combined
            self.Phdr.clear()
        return self.Phdr_d

    def Elf_Shdr(self):
        self.f.seek(self.Ehdr[12])
        for i in range(self.Ehdr[18]):
            if self.arch:
                [self.Shdr.append(self.f.read(i)) for i in Shdr64]
            else:
                [self.Shdr.append(self.f.read(i)) for i in Shdr32]
            self.Shdr = list(map(lambda f: toInt(f, self.little_endian), self.Shdr))
            combined = OrderedDict(zip(Shdr_names, self.Shdr))
            self.Shdr_d[i] = combined
            self.Shdr.clear()
        return self.Shdr_d



if __name__ == '__main__':
    x = elfstruct(open('server', 'r+b'))
    print(x.Elf_Ehdr())
    #print(x.Elf_Phdr())
    #print(x.Elf_Shdr())
