#!/usr/bin/env python
import sys


def usage():
    """Prints the correct usage of the module.

    Prints an example of the correct usage for this module and then exits,
    in the event of improper user input.

    >>>Usage: hw1.py <file1>
    """
    print("Usage: "+sys.argv[0]+" <file1>")
    sys.exit(2)

def getFile():
    """Creates a file descriptor for a user-specified file.

    Retreives the filename from the second command line argument
    and then creates a file descriptor for it.

    Returns:
        int: A file descriptor for the newly opened file specified
        by the user.

    Raises:
        An error occured while attempting to open the file
    """ 
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        usage()
    try:
        fd = open(filename, "rb")
        return fd
    except:
        print("error opening program ") 
        sys.exit()

def partialLine(bytes):
    """Adds additional spacing so the ASCII on a shortened line lines up with preceeding lines.

    Takes the number of bytes on a short line and finds the difference 
    between a full line. This difference is then used to calculate
    the number of spaces necessary to properly align the ASCII with
    the rows above.

    >>>00000000 32 b4 51 7a 3b 3c 64 dd c3 61 da 8a ff 60 5c 9b |2.Qz;<d..a...`\.|
    >>>00000120 91 93 f7                                        |...|

    Args:
        bytes: The number of bytes currently being processed
    """
    if sys.getsizeof(bytes) < 33:
        difference = 33 - sys.getsizeof(bytes)
        while difference != 0:
            print("   ", end = "")
            difference = difference - 1

def process():
    """Forms a table with byte hex values, memory positions in hex, and associated ASCII

    Uses the file descriptor from getFile() to continually read 16 bytes
    formatting each line so that the memory position, in hex, of the first
    byte of a line, followed by all of the hex values for those bytes, and then 
    the associated ASCII values for the hex values.

    >>>00000000 32 b4 51 7a 3b 3c 64 dd c3 61 da 8a ff 60 5c 9b |2.Qz;<d..a...`\.|
    
    Raises:
        An error occured while attempting to close the file
    """
    fd = getFile()
    count = 0
    bytes = fd.read(16)
    while bytes:
        print("%08x" % count + " ", end = "")
        for b in bytes:
            print("%02x" % b + " ", end = "")
            count = count + 1
        if sys.getsizeof(bytes) < 33 and sys.getsizeof(bytes) > 17:
            partialLine(bytes)
        print("|", end = "")
        for b in bytes:
            if b > 31 and b < 127:
                print(chr(b), end = "")
            else:
                print(".", end = "")
        print("|")
        bytes = fd.read(16)
    print("%08x" % count + " ")
    try:
        fd.close()
    except:
        print("error closing program ")
        sys.exit()

def main():
    process()
if __name__=="__main__":
    main()
