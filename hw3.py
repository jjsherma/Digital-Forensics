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
        if(fd.read(2) != b'\xff\xd8'):
            print("Is not a JPG")
            fd.close()
        else:
            print("Is a JPG")
            return fd
    except:
        print("error opening program ")
        sys.exit()

def get_markers():
    offsets = []
    markers = []
    sizes = []
    fd = getFile()
    offset = 2
    bytes = fd.read(2)
    while bytes:
        """offsets.append(offset)"""
        marker = struct.unpack(">H", bytes)[0]
        """markers.append(bytes)"""
        current_size = fd.read(2)
        """sizes.append(current_size)"""
        print("[0x" + "%04X" % offset + "]" + " ", end = "")
        current_size_int = struct.unpack(">h", current_size)[0]
        exif = fd.read(6)
        indicator = offset + 10
        offset = offset + 2 + current_size_int
        print("Marker " + "0x" + "%X" % marker + " ", end = "")
        print("size=" + "0x" + "%04X" % current_size_int + " ")
        check_exif(exif, fd, indicator)
        if(marker == 65498):
            break
        fd.seek(offset)
        bytes = fd.read(2)
    
def check_exif(exif, fd, indicator):
    if(exif == b'Exif\x00\x00'):
        '''print("match")'''
        exif = fd.read(2)
        if(exif == b'MM'):
            '''print("Big Endian")'''
            exif = fd.read(2)
            exif = fd.read(4)
            IFD_offset = struct.unpack(">L", exif[0:4])[0]
            print(IFD_offset)
            fd.seek(indicator)
            exif = fd.read(IFD_offset)
            '''print(exif)'''
            exif = fd.read(2)
            '''print(exif)'''
            IFD_size = struct.unpack(">h", exif)[0]
            print("Number of IFD Entries: %d" % IFD_size)
            get_IFD(IFD_offset, IFD_size, fd, indicator)
        else:
            print("Little Endian")
            sys.exit()

def get_IFD(IFD_offset, IFD_size, fd, indicator):
    entry_count = 0
    bytes_per_component = (0, 1, 1, 2, 4, 8, 1, 1, 2, 4, 8, 4, 8)
    while entry_count < IFD_size:
        fd.seek(indicator + IFD_offset + (entry_count * 12) + 2)
        tag = fd.read(2)
        tag_int = struct.unpack(">H", tag)[0]
        tag_string = TAGS[tag_int]
        print("%x " % tag_int, end = "")
        print(tag_string + " ", end = "")
        format = fd.read(2)
        format_int = struct.unpack(">h", format)[0]
        '''print("%d" % format_int + " ", end = "")'''
        components = fd.read(4)
        components_int = struct.unpack(">L", components)[0]
        '''print("%d" % components_int + " ", end = "")'''
        entry_length = bytes_per_component[format_int] * components_int
        '''print("%d" % entry_length + " ", end = "")'''
        if(entry_length <= 4):
            IFD_data = fd.read(4)
            if(format_int == 1):
                print(struct.unpack(">B", IFD_data[0:1])[0])
            elif(format_int == 2):
                print(bytes.decode(IFD_data[0:entry_length]))
            elif(format_int == 3):
                print(struct.unpack(">%dh" % components_int, IFD_data[0:entry_length])[0])
            elif(format_int == 4):
                ulong = struct.unpack(">L", IFD_data[0:4])[0]
                print("[%d]" % ulong)
            elif(format_int == 7):
                print(struct.unpack(">%dB" % entry_length, IFD_data[0:entry_length])[0])
                print("".join("%c" % x for x in format_int))
        else:
            IFD_data = fd.read(4)
            IFD_data_offset = struct.unpack(">L", IFD_data[0:4])[0]
            fd.seek(indicator + IFD_data_offset)
            IFD_data = fd.read(entry_length)
            if(format_int == 1):
                print(struct.unpack(">B", IFD_data[0:1])[0])
            elif(format_int == 2):
                print(bytes.decode(IFD_data[0:entry_length]))
            elif(format_int == 3):
                print(struct.unpack(">%dh" % components_int, IFD_data[0:entry_length])[0])
            elif(format_int == 4):
                ulong = struct.unpack(">L", IFD_data[0:4])[0]
                print("[%d]" % ulong)
            elif(format_int == 5):
                (numerator, denominator) = struct.unpack(">LL", IFD_data[0:8])
                print("['" + "%s/%s" % (numerator, denominator) + "']")
            elif(format_int == 7):
                print(struct.unpack(">%dB" % entry_length, IFD_data[0:entry_length])[0])
                print("".join("%c" % x for x in format_int))

        entry_count += 1
    
def main():
    get_markers()

if __name__=="__main__":
  main()

