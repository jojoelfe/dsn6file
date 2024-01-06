# dsn6file

[![PyPI - Version](https://img.shields.io/pypi/v/dsn6file.svg)](https://pypi.org/project/dsn6file)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dsn6file.svg)](https://pypi.org/project/dsn6file)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)
- [Usage](#usage)

## Installation

```console
pip install dsn6file
```

## Usage

At the moment the library only supports reading dsn6 files, but not writing them.

```python
from dsn6file import DSN6File
dsn6 = DSN6File(test_data_directory / "6c10_2fofc.dsn6")
dsn6_data = dsn6.get_data()
```

## License

`dsn6file` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
