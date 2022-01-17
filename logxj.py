import socket
port = 61359
print('WAITING...')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(('0.0.0.0',port))
sock.listen(1)
connection,address = sock.accept()
print('LOGXJ:')
print(connection.recv(1024).decode('utf-8','ignore'))
connection.close()
