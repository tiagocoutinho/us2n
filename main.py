import socket
import network

def download(addr, src='main.py', dest=None, timeout=1):
    import socket
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect(addr)
        s.send(src)
        data = []
        while True:
            try:
                data.append(s.recv(4096))
            except:
                break
        if dest is None:
            dest = src
        with open(dest, 'wb') as f:
            f.write(b''.join(data))
    finally:
        s.close()


def main():
    print(50*'=')
    print('Welcome to Tiago\'s ESP32 device\n')
    print('Starting UART<->TCP bridge server...')
    try:
        import us2n
    except:
        print('Failed to import us2n')
    else:
        server = us2n.server()
        server.serve_forever()


if __name__ == '__main__':
    main()
