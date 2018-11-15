#include <cstdlib>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstring>
#include <elf.h>

/**
 * The goal of this tool is to confuse a disassembler into thinking that the
 * executable portion of the code is data and the data portion of the code is
 * executable.
 *
 * This tool will add a section table to a binary that doesn't have one. The
 * section table will be made up of 4 headers:
 *
 * - null header
 * - .data: this section covers what .text should, but we unset X and set W
 * - .text: this section covers what .data should, but we set X and unset W
 * - .shstrtab: the strings table.
 *
 * This code makes the assumption that the binary has two PF_LOAD segments in
 * the program table. One segment with PF_X set and one with PF_W set.
 */

/*
 * Edits the ELF header to indicate that there are 6 section headers and that
 * the string table is the last one.
 *
 * \param[in,out] p_data the ELF binary
 * \return true if its possible to add a section table. false otherwise
 */
bool edit_elf_header(std::string& p_data)
{
    if (p_data[0] != 0x7f || p_data[1] != 'E' || p_data[2] != 'L' ||
        p_data[3] != 'F')
    {
        return false;
    }

    Elf64_Ehdr* ehdr = reinterpret_cast<Elf64_Ehdr*>(&p_data[0]);

    if (ehdr->e_shoff != 0)
    {
        std::cerr << "The binary already has a section table." << std::endl;
        return false;
    }

    if (ehdr->e_shentsize != sizeof(Elf64_Shdr))
    {
        std::cerr << "Unexpected section header size" << std::endl;
        return false;
    }

    ehdr->e_shoff = p_data.size();
    ehdr->e_shnum = 4;
    ehdr->e_shstrndx = 3;
    return true;
}

/*
 * This finds the PF_X segment and creates a section header named .data that
 * does not have the X bit set.
 *
 * \param[in,out] p_data the ELF binary
 * \param[in,out] p_strings the section table string names
 * \return true if no error was encountered
 */
bool add_data_section(std::string& p_data, std::string& p_strings)
{
    Elf64_Ehdr* ehdr = reinterpret_cast<Elf64_Ehdr*>(&p_data[0]);
    Elf64_Phdr* phdr = reinterpret_cast<Elf64_Phdr*>(&p_data[0] + ehdr->e_phoff);

    for (int i = 0; i < ehdr->e_phnum; i++, phdr++)
    {
        if (phdr->p_type == PT_LOAD)
        {
            if ((phdr->p_flags & PF_X) == PF_X)
            {
                Elf64_Shdr data_header = {};
                data_header.sh_name = p_strings.size();
                data_header.sh_type = SHT_PROGBITS;
                data_header.sh_flags = SHF_ALLOC | SHF_WRITE;
                data_header.sh_addr = phdr->p_vaddr;
                data_header.sh_offset = phdr->p_offset;
                data_header.sh_size = phdr->p_filesz;
                data_header.sh_link = 0;
                data_header.sh_info = 0;
                data_header.sh_addralign = 4;
                data_header.sh_entsize = 0;
                p_strings.append(".data");
                p_strings.push_back('\x00');
                p_data.append(reinterpret_cast<char*>(&data_header),
                              sizeof(data_header));
            }
        }
    }
    return false;
}

/*
 * This finds the PF_W segment and creates a section header named .text that
 * has the X bit set.
 *
 * \param[in,out] p_data the ELF binary
 * \param[in,out] p_strings the section table string names
 * \return true if no error was encountered
 */
bool add_text_section(std::string& p_data, std::string& p_strings)
{
    Elf64_Ehdr* ehdr = reinterpret_cast<Elf64_Ehdr*>(&p_data[0]);
    Elf64_Phdr* phdr = reinterpret_cast<Elf64_Phdr*>(&p_data[0] + ehdr->e_phoff);

    for (int i = 0; i < ehdr->e_phnum; i++, phdr++)
    {
        if (phdr->p_type == PT_LOAD)
        {
            if ((phdr->p_flags & PF_X) == 0)
            {
                Elf64_Shdr text_header = {};
                text_header.sh_name = p_strings.size();
                text_header.sh_type = SHT_PROGBITS;
                text_header.sh_flags = SHF_ALLOC | SHF_EXECINSTR;
                text_header.sh_addr = phdr->p_vaddr;
                text_header.sh_offset = phdr->p_offset;
                text_header.sh_size = phdr->p_filesz;
                text_header.sh_link = 0;
                text_header.sh_info = 0;
                text_header.sh_addralign = 4;
                text_header.sh_entsize = 0;
                p_strings.append(".text");
                p_strings.push_back('\x00');
                p_data.append(reinterpret_cast<char*>(&text_header),
                              sizeof(text_header));
                return true;
            }
        }
    }
    return false;
}

bool append_sections(std::string& p_data)
{
    // this will contain the section name strings
    std::string strings;
    strings.push_back('\x00');

    // first section is empty
    Elf64_Shdr null_header = {};
    p_data.append(reinterpret_cast<char*>(&null_header), sizeof(null_header));

    if (!add_data_section(p_data, strings))
    {
        std::cerr << "Failed to find the executable LOAD segment" << std::endl;
        return false;
    }

    if (!add_text_section(p_data, strings))
    {
        std::cerr << "Failed to find the writable LOAD segment" << std::endl;
        return false;
    }

    // .shstrtab
    Elf64_Shdr strtab = {};
    strtab.sh_name = strings.size();
    strtab.sh_type = SHT_STRTAB;
    strtab.sh_flags = 0;
    strtab.sh_addr = 0;
    strtab.sh_offset = p_data.size() + sizeof(Elf64_Shdr);
    strtab.sh_size = 0;
    strtab.sh_link = 0;
    strtab.sh_info = 0;
    strtab.sh_addralign = 4;
    strtab.sh_entsize = 0;
    strings.append(".shstrtab");
    strings.push_back('\x00');
    strtab.sh_size = strings.size();
    p_data.append(reinterpret_cast<char*>(&strtab), sizeof(strtab));
    p_data.append(strings);

    return true;
}

int main(int p_argc, char** p_argv)
{
    if (p_argc != 2)
    {
        std::cerr << "Usage: ./fakeHeadersXBit <file path>" << std::endl;
        return EXIT_FAILURE;
    }

    std::ifstream inputFile(p_argv[1], std::ifstream::in | std::ifstream::binary);
    if (!inputFile.is_open() || !inputFile.good())
    {
        std::cerr << "Failed to ropen the provided file: " << p_argv[1] << std::endl;
        return EXIT_FAILURE;
    }

    std::string input((std::istreambuf_iterator<char>(inputFile)), std::istreambuf_iterator<char>());
    inputFile.close();

    if (!edit_elf_header(input))
    {
        return EXIT_FAILURE;
    }

    if (!append_sections(input))
    {
        return EXIT_FAILURE;
    }

    std::ofstream outputFile(p_argv[1], std::ofstream::out | std::ofstream::binary);
    if (!outputFile.is_open() || !outputFile.good())
    {
        std::cerr << "Failed to wopen the provided file: " << p_argv[1] << std::endl;
        return EXIT_FAILURE;
    }

    outputFile.write(input.data(), input.length());
    outputFile.close();
    return EXIT_SUCCESS;
}
