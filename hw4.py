#!/usr/bin/env python
import sys
import struct

"""Created by Joshua Sherman - 27486230"""

def usage():
    """Prints the correct usage of the module.

    Prints an example of the correct usage for this module and then exits,
    in the event of improper user input.

    >>>Usage: hw4.py <int> <file1>.dd
    """
    print("Usage: "+sys.argv[0]+" <offset> <file1>.dd")
    sys.exit(2)

def get_file():
    """Creates a file descriptor for a user-specified file.

    Retrieves the filename of the disk from the third command line argument
    and then creates a file descriptor for it. Also retrieves the offset
    (in sectors) to the boot sector from the second command line argument.

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
    return(fd, offset)

def parse_fat():
    """Parses the boot sector of a FAT16 Filesystem.

    Seeks to the fixed byte location of various essential data in the
    boot sector, then stores that data. After all of the data has been collected,
    it is printed to the screen in a format similar to fsstat. Assumes that each sector
    is 512 bytes.
    
    """
    results = get_file()
    fd = results[0]
    offset = results[1]
    fd.seek(510 + (512 * offset))
    FAT_check_bytes = fd.read(2)
    FAT_check = struct.unpack("<H", FAT_check_bytes)[0]
    if FAT_check != 43605:
        print("This is not a boot sector, it may be damaged, this may not be a disk, or you may have the wrong offset")
        usage()
    
    #Retrieve the OEM name
    fd.seek(3 + (512 * offset))
    oem_name_bytes = fd.read(8)
    oem_name = ""
    for b in oem_name_bytes:
        if b > 31 and b < 127:
            oem_name += chr(b)
        else:
            oem_name += "."
    #Retrieve the Volume ID
    fd.seek(39 + (512 * offset))
    volume_ID_bytes = fd.read(4)
    volume_ID = "0x"
    volume_ID_body = struct.unpack("<L", volume_ID_bytes)[0]
    volume_ID_body = format(volume_ID_body, '08x')
    volume_ID += volume_ID_body
    #Retrieve the Volume Label
    volume_label_bytes = fd.read(11)
    volume_label = ""
    for b in volume_label_bytes:
        if b > 31 and b < 127:
            volume_label += chr(b)
        else:
            volume_label += "."
    #Retrieve the File System Label
    fs_label_bytes = fd.read(8)
    fs_label = ""
    for b in fs_label_bytes:
        if b > 31 and b < 127:
            fs_label += chr(b)
        else:
            fs_label += "."
    #Retrieve the number of bytes per sector
    fd.seek(11 + (512 * offset))
    bytes_per_sector_bytes = fd.read(2)
    bytes_per_sector = struct.unpack("<H", bytes_per_sector_bytes)[0]
    #Retrieve the number of sectors per cluster
    sectors_per_cluster_bytes = fd.read(1)
    sectors_per_cluster = sectors_per_cluster_bytes[0]
    #Retrieve the size of the Reserved area
    reserved_bytes = fd.read(2)
    reserved = struct.unpack("<H", reserved_bytes)[0]
    #Retrieve the number of FATs
    numfats_bytes = fd.read(1)
    numfats = numfats_bytes[0]
    #Retrieve the number of maximum files in the root
    max_files_bytes = fd.read(2)
    max_files = struct.unpack("<H", max_files_bytes)[0]
    #Retrieve the total number of sectors
    total_sectors_bytes = fd.read(2)
    total_sectors = struct.unpack("<H", total_sectors_bytes)[0]
    fd.read(1)
    #Retrieve the size of each FAT
    fat_size_bytes = fd.read(2)
    fat_size = struct.unpack("<H", fat_size_bytes)[0]
    #Retrieve the 4-byte number of sectors if too small to fit into 2 bytes
    if total_sectors == 0:
        fd.seek(32 + (512 * offset))
        total_sectors_bytes = fd.read(4)
        total_sectors = struct.unpack("<L", total_sectors_bytes)[0]
    #Calculate the size of the root
    root_size = (max_files * 32) / (bytes_per_sector)
    root_size = round(root_size)
    #Calculate the starting sector of the Data area
    data_start = reserved + (numfats * fat_size)
    #Calculate the size of the Data area
    data_size = total_sectors - data_start
    #Calculate the type of FAT
    cluster_size = int(data_size / sectors_per_cluster) * sectors_per_cluster
    fs_type = ""
    if cluster_size < 4085:
        fs_type = "FAT12"
    if cluster_size >= 4085 and cluster_size < 65525:
        fs_type = "FAT16"
    if cluster_size >= 65525:
        fs_type = "FAT32"
    #Calculate the number of sectors not in a cluster
    noncluster_size = data_size - cluster_size
    #Print all of the information
    print("")
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
    cluster_range = int(((total_sectors - 1 - noncluster_size) - (end_position + 1 + root_size)) / 2 + 2) #Calculate the cluster range
    print("Total Cluster Range: 2 - %d " % (cluster_range)) 
def main():
    """Simply runs parse_fat withour arguments"""
    parse_fat()

if __name__=="__main__":
  main()



