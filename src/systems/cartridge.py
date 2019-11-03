import io
import os
import hashlib


#  Cartridge
#
#  A generic cartridge class to handle common operations for all ROM/cartridge types
class Cartridge:

    def __init__(self, input_stream=None):
        print("cart init")
        self.in_stream = input_stream
        try:
            self._rom_size = input_stream.getbuffer().nbytes
        except AttributeError:
            self._rom_size = 0

        self._md5_hex_str = None
        self._md5_bytes = None
        self._checksum_calculated = 0
        self._checksum_in_rom = 0
        self._header = {}

    @classmethod
    def from_file(cls, file_name):
        rom_size = os.path.getsize(file_name)
        in_stream = io.BytesIO()
        with open(file_name, "rb") as f:
            in_stream.write(f.read(rom_size))
        return cls(in_stream)

    @property
    def rom_size(self):
        return self._rom_size

    @property
    def checksum_calculated(self):
        return self._checksum_calculated

    @property
    def checksum_in_rom(self):
        return self._checksum_in_rom

    @property
    def header(self):
        return self._header

    @property
    def md5_str(self):
        return self._md5_hex_str

    @property
    def md5_bytes(self):
        return self._md5_bytes

    def calculate_md5(self):
        if self.in_stream is not None:
            self.in_stream.seek(0)
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: self.in_stream.read(4096), b""):
                hash_md5.update(chunk)
            # packed bytes
            self._md5_bytes = hash_md5.digest()
            # hex string
            self._md5_hex_str = hash_md5.hexdigest()
            return hash_md5.digest()
        else:
            print("No input file stream available")
