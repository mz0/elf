import os

class elfparser:
    def __init__(self, filename):
        self._filename = filename
        self.elf = self._open(self._filename)
        self.elf_header()
        self._elfh_l = []
        # self.program_header()


    def _open(self, filename):
        with open(filename, 'rb') as f:
            f = f.read()
            # 0x7F followed by ELF(45 4c 46)
            if f[:0x4] != bytes(b'\x7f\x45\x4c\x46'):
                raise ValueError('Not an elf file')
            return f
        raise ValueError(f'No file named "{filename}" was found')

    # elf header is always on the same place
    def elf_header(self):
        self.EI_DATA    = self.elf[0x5]
        if self.EI_DATA != 0x01 and self.EI_DATA != 0x02:
            raise ValueError('endianness is not recognized')
        self.EI_CLASS   = self.elf[0x4]
        self.EI_VERSION = self.elf[0x6]
        self.EI_OSABI   = self.elf[0x7]
        self.EI_ABIVERSION  = self.elf[0x8]
        self.EI_PAD     = self.elf[0x9:0x10]
        self.e_type     = int.from_bytes(self.elf[0x10:0x12], byteorder='little' if self.EI_DATA == 1 else 'big')
        self.e_machine  = int.from_bytes(self.elf[0x12:0x14], byteorder='little' if self.EI_DATA == 1 else 'big')
        self.e_version  = int.from_bytes(self.elf[0x14:0x18], byteorder='little' if self.EI_DATA == 1 else 'big')
        if self.EI_CLASS == 1:
            self.e_entry    = int.from_bytes(self.elf[0x18:0x1C], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phoff    = int.from_bytes(self.elf[0x1c:0x20], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shoff    = int.from_bytes(self.elf[0x20:0x24], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_flags    = int.from_bytes(self.elf[0x24:0x28], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_ehsize   = int.from_bytes(self.elf[0x28:0x2A], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phentsize= int.from_bytes(self.elf[0x2A:0x2C], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phnum    = int.from_bytes(self.elf[0x2C:0x2E], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shentsize= int.from_bytes(self.elf[0x2E:0x30], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shnum    = int.from_bytes(self.elf[0x30:0x32], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shstrndx = int.from_bytes(self.elf[0x32:0x34], byteorder='little' if self.EI_DATA == 1 else 'big')
        elif self.EI_CLASS == 2:
            self.e_entry    = int.from_bytes(self.elf[0x18:0x20], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phoff    = int.from_bytes(self.elf[0x20:0x28], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shoff    = int.from_bytes(self.elf[0x28:0x30], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_flags    = self.elf[0x30:0x34]
            self.e_ehsize   = int.from_bytes(self.elf[0x34:0x36], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phentsize= int.from_bytes(self.elf[0x36:0x38], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_phnum    = int.from_bytes(self.elf[0x38:0x3A], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shentsize= int.from_bytes(self.elf[0x3A:0x3C], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shnum    = int.from_bytes(self.elf[0x3C:0x3E], byteorder='little' if self.EI_DATA == 1 else 'big')
            self.e_shstrndx = int.from_bytes(self.elf[0x3E:0x40], byteorder='little' if self.EI_DATA == 1 else 'big')
        else:
            # call to func to parse unknown endianness
            pass
        self.parse_elf_header()


    def parse_elf_header(self):
        print('Architecture:\t\t\t%s'
         % ('x32' if self.EI_CLASS == 0x01 else
            'x64' if self.EI_CLASS == 0x02 else
            'unknown'))

        print('Endianness:\t\t\t%s'
         % ('little' if self.EI_DATA == 0x01 else
            'big'    if self.EI_DATA == 0x02 else
            'unknown'))

        print('Version:\t\t\t%s' % (self.EI_VERSION))

        print('OS/ABI:\t\t\t\t%s'
         % ('0x00, Sytem V'         if self.EI_OSABI == 0x00 else
            '0x01, HP-UX'           if self.EI_OSABI == 0x01 else
            '0x02, NetBSD'          if self.EI_OSABI == 0x02 else
            '0x03, Linux'           if self.EI_OSABI == 0x03 else
            '0x04, GNU Hurd'        if self.EI_OSABI == 0x04 else
            '0x06, Solaris'         if self.EI_OSABI == 0x06 else
            '0x07, AIX'             if self.EI_OSABI == 0x07 else
            '0x08, IRIX'            if self.EI_OSABI == 0x08 else
            '0x09, FreeBSD'         if self.EI_OSABI == 0x09 else
            '0x0A, True64'          if self.EI_OSABI == 0x0A else
            '0x0B, Novell Modesto'  if self.EI_OSABI == 0x0B else
            '0x0C, OpenBSD'         if self.EI_OSABI == 0x0C else
            '0x0D, OpenVMS'         if self.EI_OSABI == 0x0D else
            '0x0E, NonStop Kernel'  if self.EI_OSABI == 0x0E else
            '0x0F, AROS'            if self.EI_OSABI == 0x0F else
            '0x10, Fenix OS'        if self.EI_OSABI == 0x10 else
            '0x11, CloudABI'        if self.EI_OSABI == 0x11 else
            'unknown'))

        print(f'ABI VERSION:\t\t\t{self.EI_ABIVERSION}')

        print(f'padding:\t\t\t{self.EI_PAD}')

        print('Type:\t\t\t\t%s'
         % ('ET_NONE, No file type'                 if self.e_type == 0x0000 else
            'ET_REL, Relocatable file'              if self.e_type == 0x0001 else
            'ET_EXEC, Executable file'              if self.e_type == 0x0002 else
            'ET_DYN, Shared object file'            if self.e_type == 0x0003 else
            'ET_CORE, Core file'                    if self.e_type == 0x0004 else
            'ET_LOOS, Operating system-specific'    if self.e_type == 0xfe00 else
            'ET_HIOS, Operating system-specific'    if self.e_type == 0xfeff else
            'ET_LOPROC, Processor-specific'         if self.e_type == 0xff00 else
            'ET_HIPROC, Processor-specific'         if self.e_type == 0xffff else
            'unknown'))

        print('Machine:\t\t\t%s'
         % ('0x00, No specific instruction set'  if self.e_machine == 0x0000 else
            '0x02, SPARC'   if self.e_machine == 0x0002 else
            '0x03, x86'     if self.e_machine == 0x0003 else
            '0x08, MIPS'    if self.e_machine == 0x0008 else
            '0x14, PowerRC' if self.e_machine == 0x0014 else
            '0x16, S390'    if self.e_machine == 0x0016 else
            '0x28, ARM'     if self.e_machine == 0x0028 else
            '0x2A, SuperH'  if self.e_machine == 0x002A else
            '0x32, IA-64'   if self.e_machine == 0x0032 else
            '0x3E, x86-64'  if self.e_machine == 0x003E else
            '0xB7, AArch64' if self.e_machine == 0x00B7 else
            '0xF3, RISC-V'  if self.e_machine == 0x00F3 else
            'unknown'))

        print(f'Version:\t\t\t{self.e_version}')

        print(f'Entry Point:\t\t\t{hex(self.e_entry)}')

        print(f'Start of program headers:\t{hex(self.e_phoff)}')

        print(f'Start of section headers:\t{hex(self.e_shoff)}')

        print(f'Flags\t\t\t\t{self.e_flags}')

        print(f'Size of this header:\t\t{hex(self.e_ehsize)}')

        print(f'Size of a program headers:\t{hex(self.e_phentsize)}')

        print(f'Number of program headers:\t{self.e_phnum}')

        print(f'Size of section headers:\t{hex(self.e_shentsize)}')

        print(f'Number of section headers:\t{self.e_shnum}')

        print(f'Section header names address:\t{hex(self.e_shstrndx)}')

    def program_header(self):
        # The program header table tells the system how to create a process image.
        # It is found at file offset e_phoff, and consists of e_phnum entries,
        # each with size e_phentsize.
        # The layout is slightly different in 32-bit ELF vs 64-bit ELF,
        # because the p_flags are in a different structure location
        # for alignment reasons.
        self.p_type = self.elf[self.e_phoff+0x00:self.e_phoff+0x04]
        if self.EI_CLASS == 1:
            # p_flags are skipped in 32bit systems
            self.p_offset   = self.elf[self.e_phoff+0x04:self.e_phoff+0x08]
            self.p_vaddr    = self.elf[self.e_phoff+0x08:self.e_phoff+0x0C]
            self.p_paddr    = self.elf[self.e_phoff+0x0C:self.e_phoff+0x10]
            self.p_filesz   = self.elf[self.e_phoff+0x10:self.e_phoff+0x14]
            self.p_memsz    = self.elf[self.e_phoff+0x14:self.e_phoff+0x18]
            self.p_flags    = self.elf[self.e_phoff+0x18:self.e_phoff+0x1C]
            self.p_align    = self.elf[self.e_phoff+0x1C:self.e_phoff+0x20]
        elif self.EI_CLASS == 2:
            self.p_flags    = self.elf[self.e_phoff+0x04:self.e_phoff+0x08]
            self.p_offset   = self.elf[self.e_phoff+0x08:self.e_phoff+0x10]
            self.p_vaddr    = self.elf[self.e_phoff+0x10:self.e_phoff+0x18]
            self.p_paddr    = self.elf[self.e_phoff+0x18:self.e_phoff+0x20]
            self.p_filesz   = self.elf[self.e_phoff+0x20:self.e_phoff+0x28]
            self.p_memsz    = self.elf[self.e_phoff+0x28:self.e_phoff+0x30]
            self.p_align    = self.elf[self.e_phoff+0x30:self.e_phoff+0x38]

        print('Type:\tOffset\tVaddr\tPaddr')
        print(f'{self.p_type}\t{hex(self.p_offset)}\t{hex(self.p_vaddr)}\t{hex(self.p_paddr)}')






if __name__ == '__main__':
    my = elfparser('server')
