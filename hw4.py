#!/usr/bin/env python
import sys
import struct

def usage():
    """Prints the correct usage of the module.

    Prints an example of the correct usage for this module and then exits,
    in the event of improper user input.

    >>>Usage: hw3.py <file1>.jpg
    """
    print("Usage: "+sys.argv[0]+" <offset> <file1>.dd")
    sys.exit(2)

def get_file():
    """Creates a file descriptor for a user-specified file.

    Retrieves the filename of the jpg image from the second command line argument
    and then creates a file descriptor for it.

    Returns:
        int: A file descriptor for the newly opened jpg specified
        by the user.

    Raises:
        An error occured while attempting to open the file
    """
    if len(sys.argv) > 2:
        offset = sys.argv[1]
        filename = sys.argv[2]
    else:
        usage()
    try:
        fd = open(filename, "rb")
    except:
        print("error opening program ")
        sys.exit()
    try:
        offset = int(offset)
    except:
        print("error converting value")
        usage()
    fd.seek(offset)
    return(fd)

def parse_fat():
    fd = get_file()
    fd.seek(3)
    oem_name_bytes = fd.read(8)
    oem_name = ""
    for b in oem_name_bytes:
        if b > 31 and b < 127:
            oem_name += chr(b)
        else:
            oem_name += "."
    fd.seek(39)
    volume_ID_bytes = fd.read(4)
    volume_ID = "0x"
    volume_ID += "".join("%02x" % b for b in volume_ID_bytes)
    volume_label_bytes = fd.read(11)
    volume_label = ""
    for b in volume_label_bytes:
        if b > 31 and b < 127:
            volume_label += chr(b)
        else:
            volume_label += "."
    fs_label_bytes = fd.read(8)
    fs_label = ""
    for b in fs_label_bytes:
        if b > 31 and b < 127:
            fs_label += chr(b)
        else:
            fs_label += "."
    fd.seek(11)
    bytes_per_sector_bytes = fd.read(2)
    bytes_per_sector = struct.unpack("<H", bytes_per_sector_bytes)[0]
    sectors_per_cluster_bytes = fd.read(1)
    sectors_per_cluster = sectors_per_cluster_bytes[0]
    reserved_bytes = fd.read(2)
    reserved = struct.unpack("<H", reserved_bytes)[0]
    numfats_bytes = fd.read(1)
    numfats = numfats_bytes[0]
    max_files_bytes = fd.read(2)
    max_files = struct.unpack("<H", max_files_bytes)[0]
    total_sectors_bytes = fd.read(2)
    total_sectors = struct.unpack("<H", total_sectors_bytes)[0]
    fd.read(1)
    fat_size_bytes = fd.read(2)
    fat_size = struct.unpack("<H", fat_size_bytes)[0]
    if(total_sectors == 0):
        fd.seek(32)
        total_sectors_bytes = fd.read(4)
        total_sectors = struct.unpack("<L", total_sectors_bytes)[0]
    root_size = (max_files * 32) / (bytes_per_sector)
    root_size = round(root_size)
    data_start = reserved + (numfats * fat_size)
    data_size = total_sectors - data_start
    cluster_size = int(data_size / sectors_per_cluster) * sectors_per_cluster
    fs_type = ""
    if(cluster_size < 4085):
        fs_type = "FAT12"
    if(cluster_size >= 4085 and cluster_size < 65525):
        fs_type = "FAT16"
    if(cluster_size >= 65525):
        fs_type = "FAT32"
    noncluster_size = data_size - cluster_size
    print("FILE SYSTEM INFORMATION")
    print("--------------------------------------------")
    print("File System Type: " + fs_type)
    print("")
    print("OEM Name: " + oem_name)
    print("Volume ID: " + volume_ID)
    print("Volume Label (Boot Sector): " + volume_label)
    print("")
    print("File System Type Label: " + fs_type)
    print("")
    print("File System Layout (in sectors)")
    print("Total Range: 0 -", total_sectors - 1)
    print("Total Range in Image: 0 -", total_sectors - 1 - noncluster_size)
    print("* Reserved: 0 -", reserved - 1)
    print("** Boot Sector: 0")
    count = 0
    start_position = reserved
    end_position = reserved + fat_size - 1
    while count < numfats:
        print("* FAT %d: %d - %d" % (count, start_position, end_position))
        start_position += fat_size
        end_position += fat_size
        count += 1
    end_position -= fat_size
    print("* Data Area: %d - %d" % (end_position + 1, total_sectors - 1))
    print("** Root Directory: %d - %d" % (end_position + 1, end_position + 1 + root_size - 1))
    print("** Cluster Area: %d - %d" % (end_position + 1 + root_size, total_sectors - 1 - noncluster_size))
    print("** Non-clustered: %d - %d" % (total_sectors - noncluster_size, total_sectors - 1))
    print("")
    print("CONTENT INFORMATION")
    print("--------------------------------------------")
    print("Sector Size: %d bytes" % bytes_per_sector)
    print("Cluster Size: %d bytes" % (bytes_per_sector * sectors_per_cluster))
    cluster_range = int(((total_sectors - 1 - noncluster_size) - (end_position + 1 + root_size)) / 2 + 2)
    print("Total Cluster Range: 2 - %d " % (cluster_range)) 
def main():
    parse_fat()

if __name__=="__main__":
  main()



