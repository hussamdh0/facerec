import socket

HOST = '127.0.0.1'
PORT = 3002


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
for i in range(7000):
    msg = ('HEY for the: ' + str(i) + 'th time!').encode()
    s.send( msg )
    #print(msg)
    #time.sleep(0.01)