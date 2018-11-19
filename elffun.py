from elfstruct import *
from sys import exit, argv
from elfdicts import *
from elftypes import *
from collections import OrderedDict

usage = """
Usage: ./elffun.py <option(s)> <file>
This is a short python implementation of linux tool readelf with big changes.
You can still use:
    -a --all                Display all info
    -h --file-header        Display Elf header
    -l --program-headers    Display Program headers
    -S --section-headers    Display Section headers
"""

class parser:
    def __init__(self,command, filename):
        self.commands = {
        '-a':self.get_all_headers,
        '--all':self.get_all_headers,
        '-l':self.get_program_headers,
        '--program-headers':self.get_program_headers,
        '-h':self.get_file_header,
        '--file-header':self.get_file_header,
        '-S':self.get_section_headers,
        '--section-headers':self.get_section_headers,
        }
        self.command = command
        self.file = self._open(filename)
        self.headers = elfstruct(self.file)

    def _open(self, filename):
        try:
            f = open(filename, 'r+b')
            return f
        except:
            print('An error while openning a file occurred')
            exit(1)

    def get_all_headers(self):
        return 'lol'

    def get_file_header(self):
        hdr = self.headers.Elf_Ehdr()
        [print(f'{key.ljust(40)} {hex(value)}') for key, value in hdr.items()]

    def get_program_headers(self):
        hdr = self.headers.Elf_Phdr()
        print('Type\t\tFlags\tOffset\tVirtAddr\tPhysAddr\tFileSiz\tMemSiz\tAlign')
        for _, d in hdr.items():
            print(f'{d.get("Type")}\t\t{d.get("Flags")}\t{d.get("Offset")}\t{d.get("VirtAddr")}\t{d.get("PhysAddr")}\t{d.get("FileSiz")}\t{d.get("MemSiz")}\t{d.get("Align")}')

    def get_section_headers(self):
        return self.headers.Elf_Shdr()

    def parse(self):
        function = self.commands.get(self.command)
        if not function:
            print(usage)
            exit(1)
        try:
            function()
        except Exception as e:
            print(e)
            exit(1)

def main():
    if len(argv) != 3:
        print(usage)
    else:
        x = parser(argv[1], argv[2])
        x.parse()

if __name__ == '__main__':
    main()
