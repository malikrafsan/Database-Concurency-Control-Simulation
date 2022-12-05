import sys

from SimpleLocking import SimpleLocking
from FileHandler import FileHandler


def main():
    if len(sys.argv) != 2:
        print('Usage: py main.py <file-name>')
        exit(1)

    file_handler = FileHandler(sys.argv[1])
    simple_locking = SimpleLocking(file_handler)
    simple_locking.run()


if __name__ == '__main__':
    main()
