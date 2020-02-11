import io
import os
import hashlib
from datetime import datetime


class Cartridge:
    """
    A generic cartridge class to handle common operations for all ROM/cartridge types.
    """
    def __init__(self, rom_stream=None, file_name=None):
        """
        Constructor - Initializer the ROM stream
        :param rom_stream: io.BytesIO stream representing the ROM data
        :param file_name: filename, source of the io.BytesIO stream
        """
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
            now = datetime.now()
            self._file_name = "out/rom_{}.bin".format(now.strftime("%Y-%m-%d-%H-%M-%S"))

        self._md5_hex_str = None
        self._md5_bytes = None
        self._checksum_calculated = 0
        self._checksum_in_rom = 0
        self._header = {}

        self.calculate_md5()

    @classmethod
    def create_from_file(cls, file_name):
        """
        Create a cartridge object by loading a ROM from the file system.
        :param file_name: the file from which to load the ROM
        :return: named constructor
        """
        rom_size = os.path.getsize(file_name)
        in_stream = io.BytesIO()
        with open(file_name, "rb") as f:
            in_stream.write(f.read(rom_size))
        return cls(in_stream, file_name)

    @classmethod
    def create_from_stream(cls, stream, file_name=None):
        """
        Create a cartridge object by loading a ROM from an io.BytesIO stream
        :param stream: io.BytesIO stream representing the ROM data
        :param file_name: the file to write back to the file system if saved
        :return: named constructor
        """
        if not isinstance(stream, io.BytesIO):
            raise TypeError("input stream must be of type io.BytesIO")
        else:
            return cls(stream, file_name)

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

    def load_rom_from_file(self, file_name):
        """
        Load a new ROM from the file system into the cartridge object
        :param file_name: the file representing the ROM data
        :return:
        """
        self._file_name = os.path.abspath(file_name)
        self._rom_size = os.path.getsize(file_name)
        with open(file_name, "rb") as f:
            self.rom_stream.write(f.read(self._rom_size))

    def read_rom(self, size=None, address=None):
        """
        Read 'size' bytes at 'address' from the currently loaded ROM
        :param size: the number of bytes to read, default is 1
        :param address: the starting address from which to read, defaults to current stream pointer
        :return:
        """
        if size is None:
            size = 1
        if address is None:
            return self.rom_stream.read(size)
        else:
            self.rom_stream.seek(address)
            return self.rom_stream.read(size)

    def write_rom(self, data, address=None):
        """
        Write 'data' to 'address' in the currently loaded ROM. N.B. this does not modify the underlying ROM file in the
        file system - use 'save_rom_to_file' for this behaviour.
        :param data:
        :param address:
        :return:
        """
        if address is None:
            self.rom_stream.write(data)
        else:
            self.rom_stream.seek(address)
            self.rom_stream.write(data)
        self._rom_size = self.rom_stream.getbuffer().nbytes

    def save_rom_to_file(self, file_name=None):
        """
        Save the current ROM stream to file. If file_name is not specified the method will attempt to overwrite the
        file from which this ROM was orginally loaded.
        :param file_name:
        :return:
        """
        if file_name is None:
            file_to_save = self._file_name
        else:
            file_to_save = file_name
        self.rom_stream.seek(0)
        with open(file_to_save, "wb") as f:
            f.write(self.rom_stream.read())

    def calculate_md5(self):
        """
        Calculate the MD5 hash of the currently loaded ROM.
        :return:
        """
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
