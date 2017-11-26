_HOME_SERVER = '192.168.1.128', 25000

def activate_home_network():
    import network

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.active():
        sta_if.active(True)
        sta_if.connect('Freebox-62E559_EXT',
                       'focarii58-satiantis-aggeum%3-hispanam?8')
    return sta_if

# import socket; s=socket.socket(); s.connect(('192.168.1.128', 25000))
# s.send('main.py')
# with open('main.py', 'wb') as f:
#   f.write(s.recv(4096))

def save(filename='main.py', timeout=1):
    import socket
    activate_home_network()
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect(_HOME_SERVER)
        s.send(filename)
        data = []
        while True:
            try:
                data.append(s.recv(4096))
            except:
                break
        with open(filename, 'wb') as f:
            f.write(b''.join(data))
    finally:
        s.close()

if __name__ == '__main__':
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
