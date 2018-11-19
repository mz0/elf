from elfstruct import *
from sys import exit, argv
from elfdicts import *
from elftypes import *
from collections import OrderedDict

usage = """
Usage: ./elffun.py <option> <file>
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
        '-l':self.get_program_headers,
        '-h':self.get_file_header,
        '-S':self.get_section_headers,
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

    def get_file_header(self):
        print('Elf Header:')
        hdr = self.headers.Elf_Ehdr()
        [print(f'{key.ljust(40)} {hex(value)}') for key, value in hdr.items()]
        print('\n')

    def get_program_headers(self):
        hdr = self.headers.Elf_Phdr()
        print("Program headers:")
        print('Type\t\tFlags\t\tOffset\t\tVirtAddr\tPhysAddr\tFileSiz\t\tMemSiz\t\tAlign')
        for _, d in hdr.items():
            for _, v in d.items():
                print(f'{hex(v).ljust(16)}', end='')
            print()
        print('\n')

    def get_section_headers(self):
        hdr = self.headers.Elf_Shdr()
        print(f'Section headers:\n{"[Num]".ljust(12)}',end='')
        [print(f'{name.ljust(12)}', end='') for name in Shdr_names]
        print()
        for num, d in hdr.items():
            print(f'{str([num]).ljust(12)}', end='')
            for _, v in d.items():
                print(f'{hex(v).ljust(12)}', end='')
            print()
        print('\n')

    def get_all_headers(self):
        self.get_file_header()
        self.get_program_headers()
        self.get_section_headers()

    def parse(self):
        function = self.commands.get(self.command)
        try:
            function()
        except:
            print(usage)

def main():
    if len(argv) != 3:
        print(usage)
    else:
        x = parser(argv[1], argv[2])
        x.parse()

if __name__ == '__main__':
    main()
