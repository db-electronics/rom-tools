from tests.fixtures import *

from random import randint
from src.systems.genesis import Genesis


def test_checksum_calculation(genesis, in_stream_240p):
    genesis.calculate_checksum(in_stream_240p)
    assert genesis.checksum_in_rom == genesis.checksum_calculated


def test_checksum_bad_calculation(genesis, in_stream_240p):
    junk_size = 1024
    # add junk data at the end
    in_stream_240p.write(bytes([randint(0, 255) for n in range(junk_size)]))
    assert genesis.checksum_in_rom != genesis.calculate_checksum(in_stream_240p)
