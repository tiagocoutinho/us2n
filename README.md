# micropython ESP32 serial to tcp server

A micropython server running on an ESP32 which acts as a bridge
between UART and TCP.

## Installation

Follow steps to install *esptool* and *micropython for ESP32*.

Then...

* clone me, oh please, clone me!

```bash
$ git clone git@github.com/tiagocoutinho/us2n
```

* Create a file called `serial.conf` with a json configuration of your UART
  (You can skip this step if you use the default configuration):

```python

import json

# This is actually the default configuration if the board has no config
conf = dict(port=1, baudrate=9600, bits=8, parity=None, stop=1)
with open('serial.conf', 'w') as f:
    json.dump(conf, f)

```

* Load the newly created `serial.conf` to your ESP32

* Load `main.py` to your ESP32

* Load `us2n.py` to your ESP32

* Connect to your ESP32

```bash
$ miniterm.py /dev/ttyUSB0 115200
```

```python
>>> import us2n
>>> server = us2n.S2NServer()
>>> server.serve_forever()
```

## Usage

If, for example, your ESP32 UART is connected to a SCPI device,
you can, from any PC:

```bash
$ nc <ESP32 Wifi IP> 8000
*IDN?
ACME Instruments, C4, 122393-2, 10-0-1

```

That's all folks!