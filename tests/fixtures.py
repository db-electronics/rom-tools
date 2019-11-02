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