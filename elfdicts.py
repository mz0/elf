CLASS = {0x01:'x32', 0x02:'x64'}
DATA = {0x01:'little', 0x02:'big'}

OSABI = {0x00:'Sytem V', 0x01:'HP-UX', 0x02:'NetBSD', 0x03:'Linux',
 0x04:'GNU Hurd', 0x06:'Solaris', 0x07:'AIX', 0x08:'IRIX', 0x09:'FreeBSD',
 0x0A:'True64', 0x0B:'Novell Modesto', 0x0C:'OpenBSD', 0x0D:'OpenVMS',
 0x0E:'NonStop Kernel', 0x0F:'AROS', 0x10:'Fenix OS', 0x11:'CloudABI'}

type = {0x0000:'ET_NONE, No file type',
        0x0001:'ET_REL, Relocatable file',
        0x0002:'ET_EXEC, Executable file',
        0x0003:'ET_DYN, Shared object file',
        0x0004:'ET_CORE, Core file',
        0xfe00:'ET_LOOS, Operating system-specific',
        0xfeff:'ET_HIOS, Operating system-specific',
        0xff00:'ET_LOPROC, Processor-specific',
        0xffff:'ET_HIPROC, Processor-specific'}

machine = {0x0000:'0x00, No specific instruction set',
           0x0002:'0x02, SPARC', 0x0003:'0x03, x86',
           0x0008:'0x08 MIPS', 0x0014:'0x14, PowerRC',
           0x0016:'0x16, S390', 0x0028:'0x28, ARM',
           0x002A:'0x2A, SuperH', 0x0032:'0x32, IA-64',
           0x003E:'0x3E, x86-64', 0x00B7:'0xB7, AArch64'}

Ehdr_names = ['Magic:', 'Architecture:', 'Endianness:', 'Version:', 'OSABI:',
              'ABIVersion:', 'Padding:', 'Type:', 'Machine:',
              'Version:', 'Entry Point:', 'Start of program headers:',
              'Start of section headers:', 'Flags:', 'Size of this header:',
              'Size of a program headers:', 'Number of program headers:',
              'Size of section headers:', 'Number of section headers:',
              'Section header names address:']

Phdr64_names = ['Type', 'Flags', 'Offset', 'VirtAddr', 'PhysAddr', 'FileSiz',
                'MemSiz', 'Align']

Phdr32_names = ['Type', 'Offset', 'VirtAddr', 'PhysAddr', 'FileSiz', 'MemSiz',
                'Flags', 'Align']

Shdr_names = ['Name:', 'Type:', 'Flags:', 'Virtual address of the section in memory:',
              'Offset of the section:', 'Size of the section:',
              'Link, index of the section:', 'Extra information about the section:',
              'Alignment:', 'Size for each Entry:']

Ehdr64 = [4, 1, 1, 1, 1, 1, 7, 2, 2, 4, 8, 8, 8, 4, 2, 2, 2, 2, 2, 2]
Ehdr32 = [4, 1, 1, 1, 1, 1, 7, 2, 2, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2]

Phdr64 = [4, 4, 8, 8, 8, 8, 8, 0, 8]
Phdr32 = [4, 0, 4, 4, 4, 4, 4, 4, 4]

Shdr64 = [4, 4, 8, 8, 8, 8, 4, 4, 8, 8]
Shdr32 = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
