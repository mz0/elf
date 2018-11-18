from elfstruct import *
from sys import exit, argv
from elfdicts import *
from elftypes import *
from collections import OrderedDict

usage = """
Usage: ./elffun.py <option(s)> <file>
This is a short python implementation of linux tool readelf with big changes.
You still can use:
    -a --all                Display all info
    -h --file-header        Display Elf header
    -l --program-headers    Display Program headers
    -S --section-headers    Display Section headers
    -t --section-details    Display The section details
"""

class parser:
    def __init__(self, filename):
        self.file = self._open(filename)
        self.Ehdr = OrderedDict()
        self.getheaders()

    def getheaders(self):
        self.headers = elfstruct(self.file)
        self.Ehdr = self.headers.Elf_Ehdr()
        self.Phdr = self.headers.Elf_Phdr()
        self.Shdr = self.headers.Elf_Shdr()

    def _open(self, filename):
        try:
            f = open(filename, 'r+b')
            return f
        except:
            print('An error while openning a file occurred')
            exit(1)

def main():
    if len(argv) == 3:
        print(usage)
        exit(0)
    x = parser('server')
    print(x.Ehdr)

if __name__ == '__main__':
    main()
