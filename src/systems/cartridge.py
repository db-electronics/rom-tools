import io
import os
import hashlib


class Cartridge:
    """A generic cartridge class to handle common operations for all ROM/cartridge types
    """
    def __init__(self, rom_stream=None, file_name=None):

        # if no ROM stream was specified, create an empty one
        try:
            rom_stream.seek(0)
            self._rom_size = rom_stream.getbuffer().nbytes
            self.rom_stream = rom_stream
        except AttributeError:
            self.rom_stream = io.BytesIO()
            self._rom_size = 0

        if file_name is not None:
            self._file_name = os.path.abspath(file_name)
        else:
            self._file_name = None

        self._md5_hex_str = None
        self._md5_bytes = None
        self._checksum_calculated = 0
        self._checksum_in_rom = 0
        self._header = {}

        self.calculate_md5()

    @classmethod
    def create_from_file(cls, file_name):
        rom_size = os.path.getsize(file_name)
        in_stream = io.BytesIO()
        with open(file_name, "rb") as f:
            in_stream.write(f.read(rom_size))
        return cls(in_stream, file_name)

    @classmethod
    def create_from_stream(cls, stream):
        return cls(stream)

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

    def load_rom(self, file_name):
        self._rom_size = os.path.getsize(file_name)
        with open(file_name, "rb") as f:
            self.rom_stream.write(f.read(self._rom_size))

    def read_rom(self, size=None, address=None):
        if size is None:
            size = 1
        if address is None:
            return self.rom_stream.read(size)
        else:
            self.rom_stream.seek(address)
            return self.rom_stream.read(size)

    def write_rom(self, data, address=None):
        if address is None:
            self.rom_stream.write(data)
        else:
            self.rom_stream.seek(address)
            self.rom_stream.write(data)
        self._rom_size = self.rom_stream.getbuffer().nbytes

    def calculate_md5(self):
        if self.rom_stream is not None:
            self.rom_stream.seek(0)
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: self.rom_stream.read(1024), b""):
                hash_md5.update(chunk)
            # packed bytes
            self._md5_bytes = hash_md5.digest()
            # hex string
            self._md5_hex_str = hash_md5.hexdigest()
            return hash_md5.digest()
        else:
            print("No input file stream available")
