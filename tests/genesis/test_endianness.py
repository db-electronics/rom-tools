import pytest
import io

from random import randint
from src.systems.genesis import Genesis


@pytest.fixture
def rom_header_file():
    return "tests/genesis/rom_header.bin"


@pytest.fixture
def input_endianness_pattern():
    return bytes([n for n in range(16)])


@pytest.fixture
def expected_endianness_output():
    return b'\x01\x00\x03\x02\x05\x04\x07\x06\t\x08\x0b\n\r\x0c\x0f\x0e'


param_stream_sizes = [n for n in range(1001, 2001, 250)]
@pytest.mark.parametrize("stream_sizes", param_stream_sizes)
def test_in_stream_not_even(stream_sizes):
    # create an input stream with an odd number of bytes
    in_stream = io.BytesIO(bytes([randint(0, 255) for n in range(stream_sizes)]))
    cart = Genesis.create_from_stream(in_stream)
    out_stream = io.BytesIO()
    with pytest.raises(ValueError):
        cart.convert_endianness(out_stream)


# @pytest.mark.skip("WIP")
def test_endianness(rom_header_file, input_endianness_pattern, expected_endianness_output):
    cart = Genesis.create_from_file(rom_header_file)
    cart.write_rom(input_endianness_pattern)
    out_stream = io.BytesIO()
    cart.convert_endianness(out_stream)
    # get size of outstream
    compare_size = out_stream.getbuffer().nbytes - Genesis.header_size
    out_stream.seek(Genesis.rom_start_address)
    assert out_stream.read(compare_size) == expected_endianness_output



