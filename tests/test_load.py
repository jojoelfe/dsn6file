from pathlib import Path

import mrcfile  # type: ignore
import numpy as np
from dsn6file import DSN6File

test_data_directory = Path(__file__).parent / "data"


def test_load_header():
    """Test loading a DSN6 file."""
    dsn6 = DSN6File(test_data_directory / "6c10_2fofc.dsn6")
    assert dsn6.header.start == (-21, -10, 33)
    assert dsn6.header.extent == (83, 122, 90)
    assert dsn6.header.sampling_rate == (104, 104, 288)
    assert np.allclose(np.array(dsn6.header.unit_cell), np.array((57.675, 57.675, 159.175, 90.0, 90.0, 90.0)))
    assert dsn6.header.density_a == 21.08
    assert dsn6.header.density_c == 47
    assert dsn6.header.unit_cell_scaling_factor == 80
    assert dsn6.header.density_a_scaling_factor == 100


def test_load_data():
    dsn6 = DSN6File(test_data_directory / "6c10_2fofc.dsn6")
    dsn6_data = dsn6.get_data()
    with mrcfile.open(test_data_directory / "6c10_2fofc.mrc", permissive=True) as mrc:
        mrc_data = mrc.data
    assert np.allclose(dsn6_data, mrc_data)
