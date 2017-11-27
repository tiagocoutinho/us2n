# micropython ESP32 UART to TCP bridge

A micropython server running on an ESP32 which acts as a bridge
between UART and TCP (LAN/WLAN).

## Installation

Follow steps to install *esptool* and *micropython for ESP32*.

Then...

* clone me, oh please, clone me!

```bash
$ git clone git@github.com/tiagocoutinho/us2n
```

* Create a file called `us2n.json` with a json configuration:

```python

import json

config = {
    "name": "SuperESP32",
    "verbose": False,
    "wlan": {
        "sta": {
            "essid": "<name of your access point>",
            "password": "<password of your access point>",
        },
    },
    "bridges": [
        {
            "tcp": {
                "bind": ["", 8000],
            },
            "uart": {
                "port": 1,
                "baudrate": 9600,
                "bits": 8,
                "parity": None,
                "stop": 1,
            },
        },
    ],
}

with open('us2n.json', 'w') as f:
    json.dump(config, f)

```

* Include in your `main.py`:

```python
import us2n
server = us2n.server()
server.serve_forever()
```

* Load the newly created `us2n.json` to your ESP32

* Load `us2n.py` to your ESP32

* Load `main.py` to your ESP32

* Press reset

The server board should be ready to accept requests in a few seconds.


## Usage

Now, if, for example, your ESP32 UART is connected to a SCPI device,
you can, from any PC:

```bash
$ nc <ESP32 Wifi IP> 8000
*IDN?
ACME Instruments, C4, 122393-2, 10-0-1

```

That's all folks!