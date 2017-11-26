# us2n.py

import os
import select
import socket
import machine


def _UART(port=1, baudrate=9600, bits=8, parity=None, stop=1):
    uart = machine.UART(port, baudrate)
    uart.init(baudrate, bits=bits, parity=parity, stop=stop)
    return uart


def UART():
    import ujson
    kwargs = dict(port=1, baudrate=9600, bits=8, parity=None, stop=1)
    try:
        with open('serial.conf', 'r') as conf:
            kwargs.update(json.load(conf))
    except:
        print("Failed to load 'serial.conf'. Falling back to default config")
    return _UART(**kwargs)


class S2NServer:

    def __init__(self, bind=('', 8000)):
        self.bind = bind

    def serve_forever(self):
        try:
            self._serve_forever()
        except KeyboardInterrupt:
            print('Ctrl-C pressed. Bailing out')

    def _serve_forever(self):
        tcp_server = socket.socket()
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #    tcp_server.setblocking(False)
        tcp_server.bind(self.bind)
        tcp_server.listen(5)
        print('server listening at ', self.bind)

        fds = [tcp_server]
        serial_line = None
        tcp_client, addr_client = None, None

        try:
            while True:
                rlist, _, xlist = select.select(fds, (), fds)
                if xlist:
                    print('errors. bailing out')
                    continue
                for fd in rlist:
                    if fd == tcp_server:
                        if tcp_client:
                            print('Closing previous client ', addr_client)
                            tcp_client.close()
                        if serial_line:
                            serial_line.deinit()
                        tcp_client, addr_client = tcp_server.accept()
                        print('new connection from ', addr_client)
                        serial_line = UART()
                        fds = [tcp_server, tcp_client, serial_line]
                        break
                    elif fd == serial_line:
                        data = serial_line.read()
                        if tcp_client:
                            print('UART->TCP %r' % data)
                            tcp_client.sendall(data)
                    elif fd == tcp_client:
                        data = tcp_client.recv(4096)
                        if data:
                            print('TCP->UART %r' % data)
                            serial_line.write(data)
                        else:
                            print('client ', addr_client, ' disconnected')
                            fds = [tcp_server]
                            serial_line = None
                            tcp_client, addr_client = None, None
        finally:
            tcp_server.close()
