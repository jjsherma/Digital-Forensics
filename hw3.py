#!/usr/bin/env python
import sys
import struct

TAGS={        0x100:  "ImageWidth",
        0x101:  "ImageLength",
        0x102:  "BitsPerSample",
        0x103:  "Compression",
        0x106:  "PhotometricInterpretation",
        0x10A:  "FillOrder",
        0x10D:  "DocumentName",
        0x10E:  "ImageDescription",
        0x10F:  "Make",
        0x110:  "Model",
        0x111:  "StripOffsets",
        0x112:  "Orientation",
        0x115:  "SamplesPerPixel",
        0x116:  "RowsPerStrip",
        0x117:  "StripByteCounts",
        0x11A:  "XResolution",
        0x11B:  "YResolution",
        0x11C:  "PlanarConfiguration",
        0x128:  "ResolutionUnit",
        0x12D:  "TransferFunction",
        0x131:  "Software",
        0x132:  "DateTime",
        0x13B:  "Artist",
        0x13E:  "WhitePoint",
        0x13F:  "PrimaryChromaticities",
        0x156:  "TransferRange",
        0x200:  "JPEGProc",
        0x201:  "JPEGInterchangeFormat",
        0x202:  "JPEGInterchangeFormatLength",
        0x211:  "YCbCrCoefficients",
        0x212:  "YCbCrSubSampling",
        0x213:  "YCbCrPositioning",
        0x214:  "ReferenceBlackWhite",
        0x828F: "BatteryLevel",
        0x8298: "Copyright",
        0x829A: "ExposureTime",
        0x829D: "FNumber",
        0x83BB: "IPTC/NAA",
        0x8769: "ExifIFDPointer",
        0x8773: "InterColorProfile",
        0x8822: "ExposureProgram",
        0x8824: "SpectralSensitivity",
        0x8825: "GPSInfoIFDPointer",
        0x8827: "ISOSpeedRatings",
        0x8828: "OECF",
        0x9000: "ExifVersion",
        0x9003: "DateTimeOriginal",
        0x9004: "DateTimeDigitized",
        0x9101: "ComponentsConfiguration",
        0x9102: "CompressedBitsPerPixel",
        0x9201: "ShutterSpeedValue",
        0x9202: "ApertureValue",
        0x9203: "BrightnessValue",
        0x9204: "ExposureBiasValue",
        0x9205: "MaxApertureValue",
        0x9206: "SubjectDistance",
        0x9207: "MeteringMode",
        0x9208: "LightSource",
        0x9209: "Flash",
        0x920A: "FocalLength",
        0x9214: "SubjectArea",
        0x927C: "MakerNote",
        0x9286: "UserComment",
        0x9290: "SubSecTime",
        0x9291: "SubSecTimeOriginal",
        0x9292: "SubSecTimeDigitized",
        0xA000: "FlashPixVersion",
        0xA001: "ColorSpace",
        0xA002: "PixelXDimension",
        0xA003: "PixelYDimension",
        0xA004: "RelatedSoundFile",
        0xA005: "InteroperabilityIFDPointer",
        0xA20B: "FlashEnergy",                  # 0x920B in TIFF/EP
        0xA20C: "SpatialFrequencyResponse",     # 0x920C    -  -
        0xA20E: "FocalPlaneXResolution",        # 0x920E    -  -
        0xA20F: "FocalPlaneYResolution",        # 0x920F    -  -
        0xA210: "FocalPlaneResolutionUnit",     # 0x9210    -  -
        0xA214: "SubjectLocation",              # 0x9214    -  -
        0xA215: "ExposureIndex",                # 0x9215    -  -
        0xA217: "SensingMethod",                # 0x9217    -  -
        0xA300: "FileSource",
        0xA301: "SceneType",
        0xA302: "CFAPattern",                   # 0x828E in TIFF/EP
        0xA401: "CustomRendered",
        0xA402: "ExposureMode",
        0xA403: "WhiteBalance",
        0xA404: "DigitalZoomRatio",
        0xA405: "FocalLengthIn35mmFilm",
        0xA406: "SceneCaptureType",
        0xA407: "GainControl",
        0xA408: "Contrast",
        0xA409: "Saturation",
        0xA40A: "Sharpness",
        0xA40B: "DeviceSettingDescription",
        0xA40C: "SubjectDistanceRange",
        0xA420: "ImageUniqueID",
        0xA432: "LensSpecification",
        0xA433: "LensMake",
        0xA434: "LensModel",
        0xA435: "LensSerialNumber"
}

def usage():
    """Prints the correct usage of the module.

    Prints an example of the correct usage for this module and then exits,
    in the event of improper user input.

    >>>Usage: hw3.py <file1>.jpg
    """
    print("Usage: "+sys.argv[0]+" <file1>.jpg")
    sys.exit(2)

def getFile():
    """Creates a file descriptor for a user-specified file.

    Retrieves the filename of the jpg image from the second command line argument
    and then creates a file descriptor for it.

    Returns:
        int: A file descriptor for the newly opened jpg specified
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
    except:
        print("error opening program ")
        sys.exit()
    if(fd.read(2) != b'\xff\xd8'): #checks if file passed in is a jpg
        fd.close()
        usage()
    else:
        return fd


def get_markers():
    """Gets the markers in the jpg.

    Uses the file descriptor to locate the markers of the jpg. Prints the markers' locations from
    the start of the file, the names of the markers, and their sizes, all in hex format. Uses the sizes
    of the markers to locate the other markers. Once a marker is found, it gets passed to check_exif.

    >>[0x04F2] Marker 0xFFE1 size=0x0A0D

    """
    fd = getFile()
    offset = 2 #starting location of marker
    bytes = fd.read(2)
    while bytes:
        marker = struct.unpack(">H", bytes)[0]
        current_size = fd.read(2)
        print("[0x" + "%04X" % offset + "]" + " ", end = "")
        current_size_int = struct.unpack(">h", current_size)[0] #size of marker
        exif = fd.read(6)
        indicator = offset + 10
        offset = offset + 2 + current_size_int #Location of next marker
        print("Marker " + "0x" + "%X" % marker + " ", end = "")
        print("size=" + "0x" + "%04X" % current_size_int + " ")
        check_exif(exif, fd, indicator)
        if(marker == 65498): #Once we reach 0xFFDA, we are at the end
            break
        fd.seek(offset)
        bytes = fd.read(2)
    fd.close()
    
def check_exif(exif, fd, indicator):
    """Checks if a specific marker contains EXIF data and that it is Big Endian.
    
    Checks if a marker contains EXIF data by checking if it contains the EXIF bytes.
    Next, the EXIF data is checked to ensure that it is Big Endian. If it is Little Endian, the 
    file descriptor is closed and we exit. Endianness is checked by looking for specific bytes, in
    this case, 'MM'. The location of the first M is also stored for later.
    
    Args:
        exif: the bytes used to check if the marker contains EXIF data.
        fd: The file descriptor for the jpg.
        indicator: If this marker contains EXIF data, indicator points to the first 'M'

    >>Number of IFD Entries: 9

    """
    if(exif == b'Exif\x00\x00'):
        exif = fd.read(2)
        if(exif == b'MM'):
            exif = fd.read(2)
            exif = fd.read(4)
            IFD_offset = struct.unpack(">L", exif[0:4])[0] # Distance from first 'M' to IFD
            fd.seek(indicator) #Return to first 'M'
            exif = fd.read(IFD_offset)
            exif = fd.read(2)
            IFD_size = struct.unpack(">h", exif)[0] # Number of IFD entries
            print("Number of IFD Entries: %d" % IFD_size)
            get_IFD(IFD_offset, IFD_size, fd, indicator)
        else:
            print("Does not work for Little Endian")
            fd.close()
            sys.exit()

def get_IFD(IFD_offset, IFD_size, fd, indicator):
    """Gets and prints the IFD entries and their values.

    Gets the IFD entries by using the formula indicator + IFD_offset + 
    (entry_count * 12) + 2. Gets the entries' keys by reading in the bytes and looking
    them up in the TAGS dictionary. The entries' names are printed in hex and then converted
    into string format. The data of the entries' are converted into string format and printed
    based upon their format type.

    Args:
        IFD_offset: The distance from the first 'M' to the IFD
        IFD_size: The number of entries in the IFD
        fd: The open file descriptor for the jpg
        indicator: The location of the first 'M'

    >>10f Make Apple
    >>110 Model iPhone 5
    >>11a XResolution ['72/1']
    >>11b YResolution ['72/1']
    >>128 ResolutionUnit 2
    >>131 Software 8.1.2
    >>132 DateTime 2015:01:10 16:18:44
    >>8769 ExifIFDPointer [180]
    >>8825 GPSInfoIFDPointer [978]

    """
    entry_count = 0 
    bytes_per_component = (0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8)
    while entry_count < IFD_size:
        fd.seek(indicator + IFD_offset + (entry_count * 12) + 2)
        tag = fd.read(2)
        tag_int = struct.unpack(">H", tag)[0]
        try:
            tag_string = TAGS[tag_int]
        except KeyError: #Tag key is not in dictionary
            print("Error retreiving value from dictionary; invalid key")
            sys.exit()
        print("%x " % tag_int, end = "")
        print(tag_string + " ", end = "")
        format = fd.read(2)
        format_int = struct.unpack(">h", format)[0]
        components = fd.read(4) #number of bytes for the data
        components_int = struct.unpack(">L", components)[0]
        entry_length = bytes_per_component[format_int] * components_int
        if(entry_length <= 4): #if length is less than or equal to for, need not search for data
            IFD_data = fd.read(4)
            if(format_int == 1): #Unsigned byte
                print(struct.unpack(">B", IFD_data[0:1])[0])
            elif(format_int == 2): #ASCII String
                print(bytes.decode(IFD_data[0:entry_length]))
            elif(format_int == 3): #Unsigned Short
                print(struct.unpack(">%dh" % components_int, IFD_data[0:entry_length])[0])
            elif(format_int == 4): #Unsigned Long
                ulong = struct.unpack(">L", IFD_data[0:4])[0]
                print("[%d]" % ulong)
            elif(format_int == 7): #Undefined (raw)
                value = struct.unpack(">%dB" % entry_length, IFD_data[0:entry_length])
                print("".join("%c" % x for x in value))
        else: #Length is too long, so we use the offset to find the data
            IFD_data = fd.read(4)
            IFD_data_offset = struct.unpack(">L", IFD_data[0:4])[0]
            fd.seek(indicator + IFD_data_offset)
            IFD_data = fd.read(entry_length)
            if(format_int == 1): #Unisgned byte
                print(struct.unpack(">B", IFD_data[0:1])[0])
            elif(format_int == 2): #ASCII String
                print(bytes.decode(IFD_data[0:entry_length]))
            elif(format_int == 3): #Unsigned Short
                print(struct.unpack(">%dh" % components_int, IFD_data[0:entry_length])[0])
            elif(format_int == 4): #Unsigned Long
                ulong = struct.unpack(">L", IFD_data[0:4])[0]
                print("[%d]" % ulong)
            elif(format_int == 5): #Unsigned Rational
                (numerator, denominator) = struct.unpack(">LL", IFD_data[0:8])
                print("['" + "%s/%s" % (numerator, denominator) + "']")
            elif(format_int == 7): #Undefined (raw)
                value = struct.unpack(">%dB" % entry_length, IFD_data[0:entry_length])
                print("".join("%c" % x for x in value))

        entry_count += 1
    
def main():
    """Simply runs with user-defined arguments"""
    get_markers()

if __name__=="__main__":
  main()

