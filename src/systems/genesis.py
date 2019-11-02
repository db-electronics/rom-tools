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
    def convert_endianness(in_stream, out_stream):

        # size of input stream
        rom_size = in_stream.getbuffer().nbytes

        if rom_size % 2 != 0:
            raise ValueError("ROM file must have an even number of bytes")

        pos = 0
        in_stream.seek(0)
        out_stream.seek(0)

        while pos < rom_size:
            bad_endian = in_stream.read(2)
            rev_endian = struct.pack('<h', *struct.unpack('>h', bad_endian))
            out_stream.write(rev_endian)
            pos += 2

    def calculate_checksum(self, in_stream):

        # size of input stream
        rom_size = in_stream.getbuffer().nbytes

        # Genesis checksums start after the header
        pos = Genesis.rom_start_address
        self.checksum_calculated = 0

        # read the ROM header's checksum value
        in_stream.seek(Genesis.header_checksum_address, 0)
        data = in_stream.read(2)
        wdata = data[0], data[1]
        self.checksum_in_rom = int.from_bytes(wdata, byteorder="big")

        # jump ahead to of ROM header
        in_stream.seek(Genesis.rom_start_address, 0)

        while pos < rom_size:
            if (rom_size - pos) >= Genesis.file_read_chunk_size:
                read_size = Genesis.file_read_chunk_size
            else:
                read_size = (rom_size - pos)

            data = in_stream.read(read_size)

            i = 0
            while i < read_size and i + 1 < read_size:
                wdata = data[i], data[i + 1]
                intval = int.from_bytes(wdata, byteorder="big")
                self.checksum_calculated = (self.checksum_calculated + intval) & 0xFFFF
                i += 2

            pos += read_size

        return self.checksum_calculated
