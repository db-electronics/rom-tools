import pytest
import io
import os

from src.systems.genesis import Genesis

rom_file_240p = "tests/genesis/240p.bin"


@pytest.fixture
def genesis():
    return Genesis()


@pytest.fixture
def in_stream_240p():
    rom_size = os.path.getsize(rom_file_240p)
    in_stream = io.BytesIO()
    with open(rom_file_240p, "rb") as f:
        in_stream.write(f.read(rom_size))
    return in_stream


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


def test_get_header(genesis, in_stream_240p, header_result_240p):
    in_stream_240p.seek(Genesis.header_start_address)
    header_stream = io.BytesIO()
    header_stream.write(in_stream_240p.read(Genesis.header_size))
    assert genesis.get_header(header_stream) == header_result_240p
