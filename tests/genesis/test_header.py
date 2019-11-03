import pytest
import io
import os

from src.systems.genesis import Genesis


@pytest.fixture
def rom_file_240p():
    return "tests/genesis/240p.bin"


@pytest.fixture
def header_result_240p():
    return {'Checksum': [31646, '0x7b9e'],
            'Console Name': 'SEGA MEGA DRIVE ',
            'Copyright': 'ARTEMIO     2014',
            'Country Support': 'JUE             ',
            'Domestic Name': '240P TEST SUITE                                 ',
            'IO Support': 'JD              ',
            'Memo': 'ARTEMIO URBINA 2014                     ',
            'Modem Support': '            ',
            'Overseas Name': '240P TEST SUITE                                 ',
            'RAM Begin': [16711680, '0xff0000'],
            'RAM End': [16777215, '0xffffff'],
            'ROM Begin': [0, '0x0'],
            'ROM End': [1048576, '0x100000'],
            'SRAM Begin': [2097152, '0x200000'],
            'SRAM End': [2097663, '0x2001ff'],
            'SRAM Support': b'  \x00\x00',
            'Serial Number': 'GM 00002501-14'}


def test_read_header(rom_file_240p, header_result_240p):
    cart = Genesis.create_from_file(rom_file_240p)
    assert cart.header == header_result_240p
