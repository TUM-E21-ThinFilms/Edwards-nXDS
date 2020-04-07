# Edwards-nXDS
Python implementation of the Edwards nXDS serial communication

## Requirements
This package runs under Python 2 or 3. However, this library depends on 
the e21_util package [https://github.com/TUM-E21-ThinFilms/E21-Util] 
(needs manual installation, not on pypi).

## Installation
Simply run

```shell
git clone https://github.com/TUM-E21-ThinFilms/Edwards-nXDS.git edwards_nxds
cd edwards_nxds/
python setup.py install
```

## Instructions

We assume the following settings of the nXDS (default settings):
```yaml
Device: /dev/ttyUSB1
Baudrate: 9600
Parity: None
Stopbits: 1
Databits: 8
Timeout: 1
```

Creating a connection to the nXDS is done via
```python
import logging

from e21_util.serial_connection import Serial
from edwards_nxds.factory import EdwardsNXDSFactory

logger = logging.get_logger("my_logger")

transport = Serial("/dev/ttyUSB1", 9600, 8, None, 1, timeout=1)
device = EdwardsNXDSFactory.create(transport, logger)
```

Starting or stopping of the nXDS is achieved by
```python
device.start_pump()
device.stop_pump()
```
For other methods, see the class `EdwardsNXDSDriver`.
