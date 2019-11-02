import io
import pytest
import os

from random import randint
from src.systems.genesis import Genesis


@pytest.fixture
def genesis():
    return Genesis()


@pytest.fixture
def rom_file():
    return "tests/genesis/240p.bin"


def test_checksum_calculation(genesis, rom_file):
    rom_size = os.path.getsize(rom_file)
    in_stream = io.BytesIO()
    with open(rom_file, "rb") as f:
        in_stream.write(f.read(rom_size))
    genesis.calculate_checksum(in_stream)
    assert genesis.checksum_in_rom == genesis.checksum_calculated


def test_checksum_bad_calculation(genesis, rom_file):
    junk_size = 1024
    rom_size = os.path.getsize(rom_file)
    in_stream = io.BytesIO()
    with open(rom_file, "rb") as f:
        in_stream.write(f.read(rom_size))
    # add junk data at the end
    in_stream.write(bytes([randint(0, 255) for n in range(junk_size)]))
    assert genesis.checksum_in_rom != genesis.calculate_checksum(in_stream)
