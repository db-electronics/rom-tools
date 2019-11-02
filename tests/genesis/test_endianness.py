import pytest
import io

from src.systems.genesis import Genesis


@pytest.fixture
def genesis():
    return Genesis()


@pytest.fixture
def input_endianness_pattern():
    return bytes([n for n in range(16)])


@pytest.fixture
def expected_endianness_output():
    return b'\x01\x00\x03\x02\x05\x04\x07\x06\t\x08\x0b\n\r\x0c\x0f\x0e'


test_stream_sizes = [n for n in range(255, 1000, 100)]


@pytest.mark.parametrize("stream_sizes", test_stream_sizes)
def test_in_stream_not_even(genesis, stream_sizes):
    # create an input stream with an odd number of bytes
    in_stream = io.BytesIO(bytes([0xFF for n in range(stream_sizes)]))
    out_stream = io.BytesIO()
    with pytest.raises(ValueError):
        genesis.convert_endianness(in_stream, out_stream)


def test_endianness(genesis, input_endianness_pattern, expected_endianness_output):
    in_stream = io.BytesIO(input_endianness_pattern)
    out_stream = io.BytesIO()
    genesis.convert_endianness(in_stream, out_stream)
    # get size of outstream
    out_stream_size = out_stream.getbuffer().nbytes
    out_stream.seek(0)
    assert out_stream.read(out_stream_size) == expected_endianness_output



