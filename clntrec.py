from image.rec.osstuff import generate_embeddings_cap
import socket
from time import sleep


HOST = '127.0.0.1'
PORT = 3003

print('rec started')
while True:
    emb = generate_embeddings_cap()
    if emb is not None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(emb.tobytes())
        print(emb)
        s.close()
    else:
        print('None')