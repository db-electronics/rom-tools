import os
import struct


class Genesis:

    header_start_address = 0x100
    header_checksum_address = 0x18E
    header_size = 0x100
    rom_start_address = 0x200

    file_read_chunk_size = 1024

    def __init__(self):
        self.checksum_calculated = 0
        self.checksum_in_rom = 0
        pass

    @staticmethod
    def convert_endianness(in_file: str, out_file: str):

        if in_file == out_file:
            raise ValueError("cannot override out_file with in_file")

        # check if ifile size exists
        if not os.path.isfile(in_file):
            raise OSError("file '{}' does not exist".format(in_file))

        file_size = os.path.getsize(in_file)
        if file_size % 2 != 0:
            raise ValueError("file {} of size {} must have an even number of bytes".format(in_file, file_size))

        pos = 0

        try:
            os.remove(out_file)
        except OSError:
            pass

        with open(out_file, "wb+") as fwrite, open(in_file, "rb") as fread:
            while pos < file_size:
                bad_endian = fread.read(2)
                rev_endian = struct.pack('<h', *struct.unpack('>h', bad_endian))
                fwrite.write(rev_endian)
                pos += 2

    def calculate_checksum(self, instream, rom_size):

        # Genesis checksums start after the header
        pos = Genesis.rom_start_address
        self.checksum_calculated = 0

        # read the ROM header's checksum value
        instream.seek(Genesis.header_checksum_address, 0)
        data = instream.read(2)
        wdata = data[0], data[1]
        self.checksum_in_rom = int.from_bytes(wdata, byteorder="big")

        # jump ahead to of ROM header
        instream.seek(Genesis.rom_start_address, 0)

        while pos < rom_size:
            if (rom_size - pos) >= Genesis.file_read_chunk_size:
                read_size = Genesis.file_read_chunk_size
            else:
                read_size = (rom_size - pos)

            data = instream.read(read_size)

            i = 0
            while i < read_size and i + 1 < read_size:
                wdata = data[i], data[i + 1]
                intval = int.from_bytes(wdata, byteorder="big")
                self.checksum_calculated = (self.checksum_calculated + intval) & 0xFFFF
                i += 2

            pos += read_size
