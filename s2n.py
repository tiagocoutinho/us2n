#

import os
import select
import socket
import logging
import argparse

import serial


log = logging.getLogger(os.path.splitext(__file__)[0])


def SerialLine(**opts):
    dtr = opts.pop('dtr')
    rts = opts.pop('rts')
    serial_line = serial.Serial(**opts)
    if dtr is not None:
        serial_line.setDTR(dtr)
    if rts is not None:
        serial_line.setRTS(rts)
    return serial_line


def server_loop(tcp_addr, serial_opts):
    tcp_server = socket.socket()
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_server.bind(tcp_addr)
    tcp_server.listen(5)
    log.info('server listening at %r', tcp_addr)

    fds = [tcp_server]
    serial_line = None
    tcp_client, addr_client = None, None

    with tcp_server:
        while True:
            rlist, _, xlist = select.select(fds, (), fds)
            if xlist:
                print('errors. bailing out')
                exit(1)
            for fd in rlist:
                if fd == tcp_server:
                    if tcp_client:
                        log.info('Closing previous client %s', addr_client)
                        tcp_client.close()
                    if serial_line:
                        serial_line.close()
                    tcp_client, addr_client = tcp_server.accept()
                    log.info('new connection from %s', addr_client)
                    serial_line = SerialLine(**serial_opts)
                    fds = [tcp_server, tcp_client, serial_line]
                    break
                elif fd == serial_line:
                    data = serial_line.read(serial_line.in_waiting)
                    if tcp_client:
                        log.debug('SL:Rx -> TCP:Tx %r', data)
                        tcp_client.sendall(data)
                elif fd == tcp_client:
                    data = tcp_client.recv(4096)
                    if data:
                        log.debug('TCP:Rx -> SL:Tx %r', data)
                        serial_line.write(data)
                    else:
                        log.debug('client %s disconnected', addr_client)
                        fds = [tcp_server]
                        serial_line = None
                        tcp_client, addr_client = None, None


def main(default_bind=':20202', default_port=None, default_baudrate=9600,
         default_bytesize=8, default_parity='N', default_stopbits=1,
         default_rts=None, default_dtr=None, default_log_level='INFO'):
    """Command line tool, entry point"""

    import argparse
    parser = argparse.ArgumentParser(description='serial to TCP daemon')
    parser.add_argument('--log-level', default=default_log_level,
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO',
                                 'DEBUG'],
                        help='log level',  type=lambda c: c.upper())

    parser.add_argument('--bind', default=default_bind,
                        help='TCP bind address (ex: ":40506")')

    parser.add_argument('port', default=default_port,
                        help="serial port name (ex: /dev/ttyUSB0")

    group = parser.add_argument_group("port settings")

    group.add_argument("--baudrate", default=default_baudrate, type=int,
                       help="set baud rate, default: %(default)s")
    group.add_argument("--bytesize", default=default_bytesize, type=int,
                       help="set bytesize default: %(default)s")
    group.add_argument("--parity",  default=default_parity,
                       type=lambda c: c.upper(),
                       choices=['N', 'E', 'O', 'S', 'M'],
                       help="set parity, one of {N E O S M}, default: N")
    group.add_argument("--stopbits", default=default_stopbits, type=int,
                       help="set stopbits default: %(default)s")
    group.add_argument("--rtscts", default=False, action="store_true",
                       help="enable RTS/CTS flow control (default off)")
    group.add_argument("--xonxoff", default=False, action="store_true",
        help="enable software flow control (default off)")
    group.add_argument("--rts", default=default_rts, type=int,
                       help="set initial RTS line state (possible: 0, 1)")
    group.add_argument("--dtr",  default=default_dtr, type=int,
        help="set initial DTR line state (possible values: 0, 1)")

    args = parser.parse_args()
    vargs = vars(args)
    log_level = vargs.pop('log_level')
    if log_level is not None:
        fmt = '%(asctime)-15s %(levelname)-5s %(name)s: %(message)s'
        logging.basicConfig(level=log_level, format=fmt)

    tcp_addr = vargs.pop('bind').rsplit(':', 1)
    if len(tcp_addr) == 1:
        tcp_addr.insert(0, '')
    tcp_addr[1] = int(tcp_addr[1])

    try:
        server_loop(tuple(tcp_addr), vargs)
    except KeyboardInterrupt:
        log.info('Ctrl-C pressed. Bailing out!')



if __name__ == '__main__':
    main()
