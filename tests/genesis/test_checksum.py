import pytest
import io
import os

from random import randint
from src.systems.genesis import Genesis


@pytest.fixture
def rom_file_240p():
    return "tests/genesis/240p.bin"


def test_checksum_calculation(rom_file_240p):
    cart = Genesis.create_from_file(rom_file_240p)
    assert cart.checksum_in_rom == cart.checksum_calculated


param_junk_length = [2**13 + 2**14, 2**15 + 2**12]
@pytest.mark.parametrize("junk_length", param_junk_length)
def test_checksum_bad_calculation(rom_file_240p, junk_length):
    cart = Genesis.create_from_file(rom_file_240p)
    # add junk data at the end
    cart.write_rom(bytes([randint(0, 255) for n in range(junk_length)]), cart.rom_size)
    # recalculate checksum
    cart.calculate_checksum()
    assert cart.checksum_in_rom != cart.checksum_calculated


def test_empty_file():
    empty_stream = io.BytesIO()
