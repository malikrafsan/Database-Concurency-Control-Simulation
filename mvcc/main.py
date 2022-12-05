import sys

from MVCC import MVCC
from FileHandler import FileHandler


def main():
    if len(sys.argv) != 2:
        raise Exception('Usage: python3 SimpleLocking.py <filename>')

    file_handler = FileHandler(sys.argv[1])
    simple_locking = MVCC(file_handler)
    simple_locking.run()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        # e.
        # raise e

