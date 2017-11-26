import os
import pty
import select
import logging
import argparse


log = logging.getLogger(os.path.splitext(__file__)[0])


class BaseReqRepDevice:

    def __init__(self, newline=b'\n'):
        self.newline = newline
        self.read_buffer = b''

    def handle_data(self, msg):
        nl = self.newline
        self.read_buffer += msg
        lines = self.read_buffer.split(nl)
        if lines[-1].endswith(nl):
            self.read_buffer = b''
        else:
            self.read_buffer = lines.pop()
        replies = (self.handle_request(line) for line in lines)
        reply = nl.join(replies)
        if reply:
            reply += nl
        return reply

    def __repr__(self):
        return type(self).__name__

    def handle_request(self, msg):
        raise NotImplementedError


class SCPI(BaseReqRepDevice):

    def handle_request(self, msg):
        if msg.upper() == b'*IDN?':
            return b'Keithley Instruments, 6485, v1022, 2003-3232'
        return b'ERR!'


def server_loop(devices):
    comms = devices.keys()
    while True:
        rlist, wlist, xlist = select.select(comms, (), comms)
        for fd in xlist:
            dev = devices[fd]
            log.error('exceptional condition on %s', dev)
        for fd in rlist:
            dev = devices[fd]
            data = os.read(fd, 4096)
            log.info('request for %s is %r', dev, data)
            reply = dev.handle_data(data)
            os.write(fd, reply)
            log.info('replied with %r', reply)


def main():
    parser = argparse.ArgumentParser(description='pty server')
    parser.add_argument('--address', default=None)
    parser.add_argument('--log-level', default='INFO', help='log level',
                        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'])
    args = parser.parse_args()
    fmt = '%(asctime)-15s %(levelname)-5s %(name)s: %(message)s'
    logging.basicConfig(level=args.log_level, format=fmt)
    address = args.address

    master, slave = pty.openpty()
    main_address = os.ttyname(slave)

    if address and address != main_address:
        if os.path.lexists(address):
            log.info('unlink %r', address)
            os.unlink(address)
        addr_path, addr_name = os.path.split(address)
        if not os.path.exists(addr_path):
            log.info('create path %r', addr_path)
            os.makedirs(addr_path)
        log.info('create link %r to %r', address, main_address)
        os.symlink(main_address, address)
    else:
        address = main_address

    log.info('Ready to accept request at %r', address)

    try:
        server_loop({master: SCPI()})
    except KeyboardInterrupt:
        log.info('Ctrl-C pressed. Bailing out!')


if __name__ == '__main__':
    main()
