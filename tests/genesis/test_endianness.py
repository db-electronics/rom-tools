import pytest
import os

from src.systems.genesis import Genesis


@pytest.fixture
def genesis():
    return Genesis()


@pytest.fixture
def input_file():
    in_file = "tests/in.bin"
    with open(in_file, "wb") as f:
        pass
    yield in_file
    os.remove(in_file)


@pytest.fixture
def output_file():
    out_file = "tests/out.bin"
    yield out_file
    try:
        os.remove(out_file)
    except OSError:
        # just ignore, not all fixture uses result in an out.bin file being created
        pass


def test_in_file_not_found(genesis):
    with pytest.raises(OSError):
        genesis.convert_endianness("fake_file.bin", "outfile.bin")


def test_in_file_not_even(genesis, input_file, output_file):
    with open(input_file, "wb") as f:
        f.write(bytes([n for n in range(17)]))
    with pytest.raises(ValueError):
        genesis.convert_endianness(input_file, output_file)


def test_in_file_equals_out_file(genesis, input_file):
    with pytest.raises(ValueError):
        genesis.convert_endianness(input_file, input_file)


def test_endianness(genesis, input_file, output_file):
    with open(input_file, "wb") as f:
        f.write(bytes([n for n in range(16)]))
    genesis.convert_endianness(input_file, output_file)
    with open(output_file, "rb") as f:
        assert f.read(16) == b'\x01\x00\x03\x02\x05\x04\x07\x06\t\x08\x0b\n\r\x0c\x0f\x0e'

