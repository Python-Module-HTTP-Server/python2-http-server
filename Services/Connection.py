
name = "Service:Connection@{port}:{socket_type}:{transferring_protocol}"

if __name__ == '__main__':
	import sys
	print 'Executable', sys.executable
	print 'Prefix', sys.exec_prefix
	print 'Executing in testing mode'
	print 'Argv:', sys.argv
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
	try:
		socket_type = sys.argv[2]
	except IndexError:
		socket_type = 'ipv4'
	try:
		transferring_protocol = sys.argv[3]
	except IndexError:
		transferring_protocol = 'tcp'
	name = name.format(port = port, socket_type = socket_type, transferring_protocol = transferring_protocol)
	print name, 'is started!'
	import socket
	if socket_type == 'ipv4':
		print 'WARN: Old socket type in future use ipv6!'
		socket_type = socket.AF_INET
		addr = ('0.0.0.0', port)
	elif socket_type == 'ipv6':
		socket_type = socket.AF_INET6
		addr = ('::', port)
	else:
		print('ERR: Unsuitable socket type: {}!\n'.format(socket_type) +
		'INFO: Enforcing to ipv4! [Other possible values: ipv6]')
		print 'WARN: Old socket type in future use ipv6!'
		socket_type = socket.AF_INET
		addr = ('0.0.0.0', port)
	if transferring_protocol == 'tcp':
		transferring_protocol = socket.SOCK_STREAM
	elif transferring_protocol == 'udp':
		transferring_protocol = socket.SOCK_DGRAM
	else:
		print('ERR: Unsuitable transferring protocol: {}!\n'.format(transferring_protocol) +
		'INFO: Enforcing to tcp! [Other possible values: udp]')
		transferring_protocol = socket.SOCK_STREAM
	listing_socket = socket.socket(socket_type, transferring_protocol)
	listing_socket.setblocking(True)
	listing_socket.bind(addr)
	listing_socket.listen(0)
	connected, address = listing_socket.accept()
	connected.setblocking(True)
	# TESTING CODE START
	print 'Signal @ {}: {}'.format(address, connected)
	return_to = connected.recvfrom(65535)
	connected.sendto('HTTP/1.1 200 OK\r\n\r\n<html><body><code>{}</code></body></html>'.format(return_to[0]), address)
	with open("../headers", 'w') as hdrs:
		hdrs.write(return_to[0])
		hdrs.close()
	# TESTING CODE END
	connected.setblocking(False)
	connected.shutdown(socket.SHUT_RDWR)
	connected.close()
	listing_socket.setblocking(False)
	listing_socket.shutdown(socket.SHUT_RDWR)
	listing_socket.close()
	print name, 'is stopped!'
	exit(0)
