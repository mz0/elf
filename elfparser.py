import os

class elfparser:
    def __init__(self, filename):
        self._filename = filename
        self.elf = self._open(self._filename)

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
        self.EI_CLASS   = self.elf[0x4]
        self.EI_DATA    = self.elf[0x5]
        self.EI_VERSION = self.elf[0x6]
        self.EI_OSABI   = self.elf[0x7]
        self.EI_ABIVERSION  = self.elf[0x8]
        self.EI_PAD     = self.elf[0x9:0x10]
        self.e_type     = self.elf[0x10:0x12]
        self.e_machine  = self.elf[0x12:0x14]
        self.e_version  = self.elf[0x14:0x18]
        if self.EI_DATA == 1:
            self.e_entry    = self.elf[0x18:0x1C]
            self.e_phoff    = self.elf[0x1c:0x20]
            self.e_shoff    = self.elf[0x20:0x24]
            self.e_flags    = self.elf[0x24:0x28]
            self.e_ehsize   = self.elf[0x28:0x2A]
            self.e_phentsize= self.elf[0x2A:0x2C]
            self.e_phnum    = self.elf[0x2C:0x2E]
            self.e_shentsize= self.elf[0x2E:0x30]
            self.e_shnum    = self.elf[0x30:0x32]
            self.e_shstrndx = self.elf[0x32:0x34]
        elif self.EI_DATA == 2:
            self.e_entry    = self.elf[0x18:0x20]
            self.e_phoff    = self.elf[0x20:0x28]
            self.e_shoff    = self.elf[0x28:0x30]
            self.e_flags    = self.elf[0x30:0x34]
            self.e_ehsize   = self.elf[0x34:0x36]
            self.e_phentsize= self.elf[0x36:0x38]
            self.e_phnum    = self.elf[0x38:0x3A]
            self.e_shentsize= self.elf[0x3A:0x3C]
            self.e_shnum    = self.elf[0x3C:0x3E]
            self.e_shstrndx = self.elf[0x3E:0x40]
        else:
            # call to func to parse unknown endianness
            pass

    def program_header(self):
        # The program header table tells the system how to create a process image.
        # It is found at file offset e_phoff, and consists of e_phnum entries,
        # each with size e_phentsize.
        # The layout is slightly different in 32-bit ELF vs 64-bit ELF,
        # because the p_flags are in a different structure location
        # for alignment reasons.
        self.p_type = self.elf[self.e_phoff+0x00:self.e_phoff+0x04]
        if self.EI_DATA == 1:
            # p_flags are skipped in 32bit systems
            self.p_offset   = self.elf[self.e_phoff+0x04:self.e_phoff+0x08]
            self.p_vaddr    = self.elf[self.e_phoff+0x08:self.e_phoff+0x0C]
            self.p_paddr    = self.elf[self.e_phoff+0x0C:self.e_phoff+0x10]
            self.p_filesz   = self.elf[self.e_phoff+0x10:self.e_phoff+0x14]
            self.p_memsz    = self.elf[self.e_phoff+0x14:self.e_phoff+0x18]
            self.p_flags    = self.elf[self.e_phoff+0x18:self.e_phoff+0x1C]
            self.p_align    = self.elf[self.e_phoff+0x1C:self.e_phoff+0x20]
        elif self.EI_DATA == 2:
            self.p_flags    = self.elf[self.e_phoff+0x04:self.e_phoff+0x08]
            self.p_offset   = self.elf[self.e_phoff+0x08:self.e_phoff+0x10]
            self.p_vaddr    = self.elf[self.e_phoff+0x10:self.e_phoff+0x18]
            self.p_paddr    = self.elf[self.e_phoff+0x18:self.e_phoff+0x20]
            self.p_filesz   = self.elf[self.e_phoff+0x20:self.e_phoff+0x28]
            self.p_memsz    = self.elf[self.e_phoff+0x28:self.e_phoff+0x30]
            self.p_align    = self.elf[self.e_phoff+0x30:self.e_phoff+0x38]






if __name__ == '__main__':
    my = elfparser('server')
