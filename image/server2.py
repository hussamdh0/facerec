import socket
import sys
import numpy as np
from time import time
from image.rec.recognition import compare_emb_min
from threading import Thread

success = 'yes I do,'
failure = b'no I do not'

tokens = []
ids = []
stamps = []


def clientHandler(c, addr):
    #print(addr, "is Connected")
    while True:
        try:
            data = c.recv(1024)
            if(data == b''):
                continue
            if(data == b'close'):
                c.close()
                break
            data = data.decode('ascii').split(',')
            print(data)
            if data[0] == 'Hello face!':
                tok = data[1]
                ts = float(data[2])
                data = c.recv(1024*2)
                if data != b'None':
                    data = np.fromstring(data, dtype=float)
                    conf, id = compare_emb_min(data)
                    print('CONF', conf, 'ID', id)
                    if conf < 0.52:
                        tokens.append(tok)
                        ids.append(id)
                        stamps.append(ts)
                        print('IDs: ', ids)
                        print('tokens: ', tokens)
                        print('stamps: ', stamps)


            if data[0] == 'do you have this token?':
                for i, tok in enumerate(tokens):
                    t = time() - stamps[i]
                    if tok == data[1] and t < 3.0 and t > 0.0:
                        c.send((success + str(ids[i])).encode())
                        print('Break')
                        break
                c.send(failure)

        except:
            print("Error. Data not sent to all clients.")
            break
    #print(addr, "is Disconnected")



HOST = ''
PORT = 3002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')


try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print ('Socket bind complete')


s.listen(10)
print ('Socket now listening')

trds = []

while 1:
    conn, addr = s.accept()
    t = Thread(target=clientHandler, args = (conn, addr))
    trds.append(t)
    t.start()

for t in trds:
    t.join()

s.close()