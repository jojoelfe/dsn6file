# SPDX-FileCopyrightText: 2024-present Johannes Elferich <jojotux123@hotmail.com>
#
# SPDX-License-Identifier: MIT
from dataclasses import dataclass

import numpy as np


@dataclass
class DSN6Header:
    start: tuple[int, int, int]
    extent: tuple[int, int, int]
    sampling_rate: tuple[int, int, int]
    unit_cell: tuple[float, float, float, float, float, float]
    density_a: float
    density_c: int
    unit_cell_scaling_factor: int
    density_a_scaling_factor: int


class DSN6File:
    """A class to represent a DSN6 file."""

    def __init__(self, filename: str) -> None:
        """Initialize a DSN6File object.

        Args:
            filename (str): The path to the DSN6 file.
        """
        self.filename = filename
        self.header = self._read_header()

    def _read_header(self) -> DSN6Header:
        # Read the first 512 bytes of the file
        header = np.fromfile(self.filename, dtype=np.int16, count=256)
        if np.little_endian:
            header = header.byteswap()
        return DSN6Header(
            start=tuple(header[0:3]),
            extent=tuple(header[3:6]),
            sampling_rate=tuple(header[6:9]),
            unit_cell=tuple(header[9:15] / header[17]),
            density_a=header[15] / header[18],
            density_c=header[16],
            unit_cell_scaling_factor=header[17],
            density_a_scaling_factor=header[18],
        )

    def get_data(self) -> np.ndarray:
        """Return the data of the DSN6 file.

        Returns:
            np.ndarray: The data of the DSN6 file.
        """
        data = np.fromfile(self.filename, dtype=np.int16, offset=512)
        data.byteswap(inplace=True)
        data = np.frombuffer(data.tobytes(), dtype=np.uint8)

        # Calculate the number of 8x8x8 subvolume
        xb, yb, zb = ((np.array(self.header.extent) - 1) / 8).astype(int) + 1
        # Setup the new array
        new_data = np.zeros((zb * 8, yb * 8, xb * 8), dtype=np.float32)

        for z in range(int(zb)):
            for y in range(int(yb)):
                for x in range(int(xb)):
                    i = (x + int(xb) * y + int(xb) * int(yb) * z) * 512
                    subvolume = (
                        data[i : i + 512].reshape(8, 8, 8).astype(int) - self.header.density_c
                    ) / self.header.density_a
                    new_data[z * 8 : z * 8 + 8, y * 8 : y * 8 + 8, x * 8 : x * 8 + 8] = subvolume
        return new_data[: self.header.extent[2], : self.header.extent[1], : self.header.extent[0]]

    def __repr__(self) -> str:
        """Return a string representation of the DSN6File object.

        Returns:
            str: A string representation of the DSN6File object.
        """
        return f"DSN6File({self.filename!r})"
