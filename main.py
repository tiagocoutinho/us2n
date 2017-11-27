import socket
import network

def activate_home_network():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
        sta_if.connect('Freebox-62E559_EXT',
                       'focarii58-satiantis-aggeum%3-hispanam?8')
    return sta_if


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
    print('Activating home network... ', end='', flush=True)
    try:
        sta = activate_home_network()
        if sta.active():
            print('[DONE]')
        else:
            print('[FAILED]')
    except Exception:
        print('[ERROR]')
    print(50*'-')


if __name__ == '__main__':
    main()
