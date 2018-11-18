from elfstruct import *
from sys import exit

class parser:
    def __init__(self, filename):
        self.file = self._open(filename)


    def getheaders(self):
        self.headers = elfstruct(self.file)
        self.Elf_Ehdr_raw = self.headers.Elf_Ehdr()
        self.Elf_Phdr_raw = self.headers.Elf_Phdr()
        self.Elf_Shdr_raw = self.headers.Elf_Shdr()

    def _open(self, filename):
        try:
            f = open(filename, 'rb')
            return f
        except:
            print('An error while openning a file occurred')
            exit(1)



if __name__ == '__main__':
    x = parser('server')
    x.getheaders()
