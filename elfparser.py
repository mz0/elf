import os

class elfparser:
    def __init__(self, filename):
        self._filename = filename
        self.elf = self._open(self._filename)



    def _open(self, filename):
        with open(filename, 'rb') as f:
            return f.read()
        raise ValueError(f'No file named {filename} was found')


if __name__ == '__main__':
    my = elfparser('server')
    print(my.elf)
