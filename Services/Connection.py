import sys, socket, thread, time
name = "Service:Connection@{port}:{socket_type}:{transferring_protocol}"

def serviceDetect():
	try:
		port = int(sys.argv[1])
	except IndexError:
		port = 8080
	except ValueError:
		service = sys.argv[1]
		if service == 'http':
			port = 80
		elif service == 'https':
			port = 443
		elif service == 'http-alt':
			port = 8080
		else:
			import random
			port = random.randint(49152, 65535)
			random = None
			del random
		service = None
		del service
	globals()['port'] = port

def socketDetect():
	try:
		socket_type = sys.argv[2]
	except IndexError:
		socket_type = 'ipv4'
	globals()['socket_type'] = socket_type

def transferring_protocolDetect():
	try:
		transferring_protocol = sys.argv[3]
	except IndexError:
		transferring_protocol = 'tcp'
	globals()['transferring_protocol'] = transferring_protocol

def setupConnection(port, socket_type, transferring_protocol):
	if socket_type == 'ipv4':
		print 'WARN: Old socket type in future use ipv6.'
		socket_type = socket.AF_INET
		addr = ('0.0.0.0', port)
	elif socket_type == 'ipv6':
		socket_type = socket.AF_INET6
		addr = ('::', port)
	else:
		print('ERR: Unsuitable socket type: {}!\n'.format(socket_type) +
		      'INFO: Enforcing to ipv4! [Other possible values: ipv6]')
		print 'WARN: Old socket type in future use ipv6.'
		socket_type = socket.AF_INET
		addr = ('0.0.0.0', port)
	if transferring_protocol == 'tcp':
		transferring_protocol = socket.SOCK_STREAM
	elif transferring_protocol == 'udp':
		transferring_protocol = socket.SOCK_DGRAM
	else:
		print('ERR: Unsuitable transferring protocol: {}.\n'.format(transferring_protocol) +
		      'INFO: Enforcing to tcp. [Other possible values: udp]')
		transferring_protocol = socket.SOCK_STREAM
	globals().update({'socket_type': socket_type, 'addr': addr, 'transferring_protocol': transferring_protocol})


def waitForSocketUnbindAndBindSocketImmidietly():
	while 1:
		try:
			listing_socket.bind(addr)
			break
		except socket.error as X:
			if X.errno != 98:
				import os.strerror as errInfo
				print errInfo(X.errno), X.errno
				errInfo = None
				del errInfo
				raise NotImplementedError("Not implemented error handler")


def threadConnection(address, connection):
	connection.setblocking(True)
	# TESTING CODE START
	
	print 'Signal @ {}: {}'.format(address, connection)
	return_to = connection.recvfrom(65535)
	#print 'First line: {}'.format(return_to[0])#.splitlines(False)[0])
	connection.sendto('HTTP/1.1 200 OK\r\n'
	                  'Content-Type: text/html\r\n'
	                  '\r\n{}'.format('<html><body>Testing code!<br /> You sended this: <code>{}</code><br /></body></html> Reply unix-time-format: {}'.format(return_to[0], time.time())), address)
	
	# TESTING CODE END
	connection.setblocking(False)
	connection.shutdown(socket.SHUT_RDWR)
	connection.close()

def getConnction():
	while 1:
		try:
			connected, address = listing_socket.accept()
			thread.start_new_thread(threadConnection, (address, connected))
		except KeyboardInterrupt:
			break
	

if __name__ == '__main__':
	port = socket_type = transferring_protocol = addr = None # for IDE
	print 'Executable', sys.executable
	print 'Arguments:', sys.argv
	print 'Executing in testing mode'
	serviceDetect()
	socketDetect()
	transferring_protocolDetect()
	name = name.format(port = port, socket_type = socket_type, transferring_protocol = transferring_protocol)
	print name, 'is started.'
	setupConnection(port, socket_type, transferring_protocol)
	print 'Setup complete.'
	listing_socket = socket.socket(socket_type, transferring_protocol)
	print 'Waiting for unbind socket.'
	waitForSocketUnbindAndBindSocketImmidietly()
	print 'Socket binded to service.'
	listing_socket.setblocking(True)
	if transferring_protocol == socket.SOCK_STREAM:
		listing_socket.listen(0)
		print 'Started listening.'
	else:
		raise NotImplementedError("NOT IMPLEMENTED YET")
	print 'Receive processor started.'
	getConnction()
	print 'Recieve processor stopped.'
	listing_socket.setblocking(False)
	listing_socket.shutdown(socket.SHUT_RDWR)
	listing_socket.close()
	print name, 'is stopped.'
	exit(0)
