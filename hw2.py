#!/usr/bin/env python
import sys

def usage():
    """Prints the correct usage of the module.

    Prints an example of the correct usage for this module and then exits,
    in the event of improper user input.

    >>>Usage: hw1.py <file1>
    """
    print("Usage: "+sys.argv[0]+" <minimum string length> <file1>")
    sys.exit(2)

def get_args():
    """Gets the filename and minimum string arguments from command line.
    
    Gets the user-defined filename and minimum string length from the
    command line. Calls usage() if not enough arguments are presented,
    or the minimum stirng length is the wrong type.

    Returns:
        fd: an open file descriptor
        minstring: the minimum string length converted into an int
    """
    if len(sys.argv) > 2:
        filename = sys.argv[2]
        minstring = sys.argv[1]
    else:
        usage()
    try:
        fd = open(filename, "rb")
    except:
        print("error opening program")
        sys.exit()
    try:
        minstring = int(minstring)
    except:
        print("error converting value")
        usage()
    return (fd, minstring)

def process():
    """Prints all strings that are at least as long as the minimum string length

    Prints all strings that are at least as long as the minimum string length by
    reading the file one byte at a time, keeping track of printable characters,
    appending them to a string, and printing that string if a non-printable
    character is presented. Also skips over the empty byte associated with
    Unicode ASCII if a valid ASCII character is presented first.

    """
    fd = get_args()[0]
    minstring = get_args()[1]
    bytes = fd.read(16)
    string = "" #String built one byte at a time
    count = 0   #The length of the building string
    unicode = False  #Activates to warn of potential incoming byte representing null character
    while bytes:
        for b in bytes:
            #Case if byte represents an ASCII character that is not a newline
            if (b > 31 and b < 127):
                count += 1
                string += chr(b)
                unicode = True

            #Case if byte represents a newline
            elif b == 10:
                count += 1
                string += chr(b)
                unicode = True

            #Case if byte represents null character, but succeeds ASCII character - skips byte
            elif b == 0 and unicode == True:
                unicode = False

            #Case if byte is non-printable, but stored string is at least minimum string length
            elif count >= minstring:
                print("go")
                print(string)
                count = 0
                string = ""

            #Case if byte is non-printable, but is not as long as minimum string length
            else:
                count = 0
                string = ""
        bytes = fd.read(16)
    try:
        fd.close()
    except:
        print("error closing program ")
        sys.exit()    

def main():
    """Simply runs with user-defined arguments"""    
    process()

if __name__=="__main__":
    main()
