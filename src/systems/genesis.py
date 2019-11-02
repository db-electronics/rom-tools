import os
import struct


class Genesis:

    header_start_address = 0x100
    header_checksum_address = 0x18E
    header_size = 0x100
    rom_start_address = 0x200

    file_read_chunk_size = 1024

    def __init__(self):
        self._checksum_calculated = 0
        self._checksum_in_rom = 0
        self._header = {}
        pass

    @property
    def checksum_calculated(self):
        return self._checksum_calculated

    @property
    def checksum_in_rom(self):
        return self._checksum_in_rom

    @property
    def header(self):
        return self._header

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
        self._checksum_calculated = 0

        # read the ROM header's checksum value
        in_stream.seek(Genesis.header_checksum_address, 0)
        data = in_stream.read(2)
        wdata = data[0], data[1]
        self._checksum_in_rom = int.from_bytes(wdata, byteorder="big")

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
                self._checksum_calculated = (self._checksum_calculated + intval) & 0xFFFF
                i += 2

            pos += read_size

        return self._checksum_calculated

    def get_header(self, in_stream):

        # the input stream is assumed to start exactly at the header data
        in_stream.seek(0)

        # clear current rom info dictionnary
        self._header.clear()
        # get console name
        self._header.update({"Console Name": in_stream.read(16).decode("utf-8", "replace")})
        # get copyright information
        self._header.update({"Copyright": in_stream.read(16).decode("utf-8", "replace")})
        # get domestic name
        self._header.update({"Domestic Name": in_stream.read(48).decode("utf-8", "replace")})
        # get overseas name
        self._header.update({"Overseas Name": in_stream.read(48).decode("utf-8", "replace")})
        # get serial number
        self._header.update({"Serial Number": in_stream.read(14).decode("utf-8", "replace")})
        # get checksum
        data = int.from_bytes(in_stream.read(2), byteorder="big")
        self._header.update({"Checksum": [data, hex(data)]})
        # get io support
        self._header.update({"IO Support": in_stream.read(16).decode("utf-8", "replace")})
        # get ROM Start Address
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"ROM Begin": [data, hex(data)]})
        # get ROM End Address
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"ROM End": [data, hex(data)]})
        # get Start of RAM
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"RAM Begin": [data, hex(data)]})
        # get End of RAM
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"RAM End": [data, hex(data)]})
        # get sram support
        self._header.update({"SRAM Support": in_stream.read(4)})
        # get start of sram
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"SRAM Begin": [data, hex(data)]})
        # get end of sram
        data = int.from_bytes(in_stream.read(4), byteorder="big")
        self._header.update({"SRAM End": [data, hex(data)]})
        # get modem support
        self._header.update({"Modem Support": in_stream.read(12).decode("utf-8", "replace")})
        # get memo
        self._header.update({"Memo": in_stream.read(40).decode("utf-8", "replace")})
        # get country support
        self._header.update({"Country Support": in_stream.read(16).decode("utf-8", "replace")})

        return self._header
