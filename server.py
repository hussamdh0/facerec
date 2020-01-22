import asyncio
import websockets
import socket
import sys
from time import sleep, time
from threading import Thread



# SHARED MEMORY
embs = []
stamps = []


# MESSAGE PASSING: HANDLE CLIENT RECOGNIZER
def rec_handler():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((RHOST, RPORT))
        s.listen(10)
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()
    while 1:
        conn, addr = s.accept()
        data = conn.recv(1024*2)
        # data = np.fromstring(data, dtype=float)
        conn.close()
        embs.append(data)
        stamps.append(time())
        if len(embs) > 10:
            del embs[0]
            del stamps[0]
        print('len(embs):', len(embs))


RHOST = ''
RPORT = 3003
t = Thread(target=rec_handler)
t.start()


# MESSAGE PASSING: HANDLE CLIENT BROWSER
async def echo(websocket, path):
    async for message in websocket:
        print('\nMessage b4 await: ')
        print(message)
        print(len(embs))
        if embs is not None:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send((message + ',' + str(stamps[-1])).encode())
            sleep(0.05)
            s.send(embs[-1])
            sleep(0.05)
            s.send(b'close')
            s.close()
            print('connect to 3002 and closed')
            messageback = 'hey, you got it!, refresh';
            await websocket.send(messageback)

HOST = '192.168.20.4'
PORT = 3002



asyncio.get_event_loop().run_until_complete(websockets.serve(echo, 'localhost', 3001))
asyncio.get_event_loop().run_forever()