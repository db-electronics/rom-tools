import os
import io
import struct
from src.systems.cartridge import Cartridge


class Genesis(Cartridge):

    header_start_address = 0x100
    header_checksum_address = 0x18E
    header_size = 0x100
    rom_start_address = 0x200

    file_read_chunk_size = 1024

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calculate_checksum()
        self.read_header()

    def __str__(self):
        return "Genesis\\Megadrive\n{}\n{} bytes".format(self.header["Domestic Name"].strip(), self.rom_size)

    def convert_endianness(self, out_stream):
        # size of input stream
        rom_size = self.rom_stream.getbuffer().nbytes

        if rom_size % 2 != 0:
            raise ValueError("ROM file must have an even number of bytes")

        pos = 0
        self.rom_stream.seek(0)
        out_stream.seek(0)

        while pos < rom_size:
            bad_endian = self.rom_stream.read(2)
            rev_endian = struct.pack('<h', *struct.unpack('>h', bad_endian))
            out_stream.write(rev_endian)
            pos += 2

    def calculate_checksum(self):

        # size of input stream
        rom_size = self.rom_stream.getbuffer().nbytes

        # Genesis checksums start after the header
        pos = Genesis.rom_start_address
        self._checksum_calculated = 0

        # read the ROM header's checksum value
        self.rom_stream.seek(Genesis.header_checksum_address, 0)
        data = self.rom_stream.read(2)
        wdata = data[0], data[1]
        self._checksum_in_rom = int.from_bytes(wdata, byteorder="big")

        # jump ahead to of ROM header
        self.rom_stream.seek(Genesis.rom_start_address, 0)

        while pos < rom_size:
            if (rom_size - pos) >= Genesis.file_read_chunk_size:
                read_size = Genesis.file_read_chunk_size
            else:
                read_size = (rom_size - pos)

            data = self.rom_stream.read(read_size)

            i = 0
            while i < read_size and i + 1 < read_size:
                wdata = data[i], data[i + 1]
                intval = int.from_bytes(wdata, byteorder="big")
                self._checksum_calculated = (self._checksum_calculated + intval) & 0xFFFF
                i += 2

            pos += read_size

        return self._checksum_calculated

    def read_header(self):

        # the input stream is assumed to start exactly at the header data
        self.rom_stream.seek(Genesis.header_start_address)

        # clear current rom info dictionnary
        self._header.clear()
        # get console name
        self._header.update({"Console Name": self.rom_stream.read(16).decode("utf-8", "replace")})
        # get copyright information
        self._header.update({"Copyright": self.rom_stream.read(16).decode("utf-8", "replace")})
        # get domestic name
        self._header.update({"Domestic Name": self.rom_stream.read(48).decode("utf-8", "replace")})
        # get overseas name
        self._header.update({"Overseas Name": self.rom_stream.read(48).decode("utf-8", "replace")})
        # get serial number
        self._header.update({"Serial Number": self.rom_stream.read(14).decode("utf-8", "replace")})
        # get checksum
        data = int.from_bytes(self.rom_stream.read(2), byteorder="big")
        self._header.update({"Checksum": [data, hex(data)]})
        # get io support
        self._header.update({"IO Support": self.rom_stream.read(16).decode("utf-8", "replace")})
        # get ROM Start Address
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"ROM Begin": [data, hex(data)]})
        # get ROM End Address
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"ROM End": [data, hex(data)]})
        # get Start of RAM
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"RAM Begin": [data, hex(data)]})
        # get End of RAM
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"RAM End": [data, hex(data)]})
        # get sram support
        self._header.update({"SRAM Support": self.rom_stream.read(4)})
        # get start of sram
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"SRAM Begin": [data, hex(data)]})
        # get end of sram
        data = int.from_bytes(self.rom_stream.read(4), byteorder="big")
        self._header.update({"SRAM End": [data, hex(data)]})
        # get modem support
        self._header.update({"Modem Support": self.rom_stream.read(12).decode("utf-8", "replace")})
        # get memo
        self._header.update({"Memo": self.rom_stream.read(40).decode("utf-8", "replace")})
        # get country support
        self._header.update({"Country Support": self.rom_stream.read(16).decode("utf-8", "replace")})

        return self._header
