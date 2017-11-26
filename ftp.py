
import os
import socket
import logging

log = logging.getLogger(os.path.splitext(__file__)[0])

logging.basicConfig(level=logging.INFO)

tcp_addr = '', 25000
tcp_server = socket.socket()
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind(tcp_addr)
tcp_server.listen(5)
log.info('server listening at %r', tcp_addr)

this_dir = os.path.dirname(os.path.abspath(__file__))

while True:
    tcp_client, addr_client = tcp_server.accept()
    log.info('new connection from %s', addr_client)
    filename = tcp_client.recv(4096).decode().strip()
    full_filename = os.path.join(this_dir, filename)
    with open(full_filename, 'rb') as f:
        tcp_client.sendfile(f)


def save(filename='main.py'):
    import socket
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
        sta_if.connect('Freebox-62E559_EXT',
                       'focarii58-satiantis-aggeum%3-hispanam?8')

    s = socket.socket()
    s.connect(('192.168.1.128', 25000))
    s.send(filename)
    data = s.recv(4096)
    with open(filename, 'wb') as f:
        f.write(data)
