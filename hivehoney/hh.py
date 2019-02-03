from __future__ import with_statement
"""
set PROXY_HOST=your_bastion_host
set SERVICE_USER=your_func_user
set LINUX_USER=your_SOID
set LINUX_PWD=your_pwd
"""
import click
import paramiko
import time, sys, os
from pprint import pprint
t_time1 = time.time()
e=sys.exit
import argparse
env=dict(os.environ)
assert 'SERVICE_USER' in env
SERVICE_USER=env['SERVICE_USER']

assert 'LINUX_USER' in env
LINUX_USER=env['LINUX_USER']

assert 'LINUX_PWD' in env
LINUX_PWD=env['LINUX_PWD']

assert 'PROXY_HOST' in env
PROXY_HOST=env['PROXY_HOST']


parser = argparse.ArgumentParser(description='Query file.')

parser.add_argument('--query_file', dest='query_file', type=str,
                                        help='Query file')
parser.add_argument('--out_file', dest='out_file', type=str, default='data_dump.csv',
                                        help='Output  csv file')
args = parser.parse_args()
if 1:
	
	assert  os.path.isfile(args.query_file), 'Query file does not exists.'
	lstat=os.stat(args.query_file)
	assert lstat.st_size>0, "Query file is empty"

	
	assert not os.path.isfile(args.out_file), 'Dump file already exists.'






nbytes = 1024*16
BASTION_HOST = PROXY_HOST #'bdgtproxyhad01h2d'
port = 22


#SERVICE_USER='gfocnnsg '

DATA_DUMP_FILE=args.out_file




			
DIR_REMOTE='/tmp'	

QUERY_FILE = args.query_file
REMOTE_QUERY_FILE= DIR_REMOTE + '/' + QUERY_FILE

PB_FILE='pbrun.exp'
REMOTE_PB_FILE=DIR_REMOTE + '/' + PB_FILE
command = '%s  %s %s %s && exit;' % (REMOTE_PB_FILE, SERVICE_USER, LINUX_PWD, REMOTE_QUERY_FILE)
print(command)
#command = 'history && exit;'
total_bytes=0
def put_file(sftp, local_file, remote_file, mode=None):

	#local_file = os.path.join(DIR_LOCAL, fname)
	#remote_file = DIR_REMOTE + '/' + fname
	print(local_file, remote_file)
	assert os.path.isfile(local_file), 'Dump file is missing.'
	try:
		sftp.unlink(remote_file)
		print('Remote file deleted')
	except FileNotFoundError as not_found:
		
		print ('Ignoring remote FileNotFoundError.')	
	#e(0)
	
	try:
		print('start transport...')
		sftp.put(local_file, remote_file)
	except :
		
		raise
	rstat=sftp.stat(remote_file)
	
	lstat=os.stat(local_file)
	print(lstat.st_size, rstat.st_size)
	assert lstat.st_size == rstat.st_size, "File size mismatch (%d<>%d)" % (lstat.st_size, rstat.st_size)
	if mode:
		sftp.chmod(remote_file, mode)
def get_data(extract_to_file):
	global total_bytes
	if 1:
		client = paramiko.Transport((BASTION_HOST, port))
		client.window_size = pow(2,35)
		client.REKEY_BYTES = pow(2, 40)
		client.REKEY_PACKETS = pow(2, 40)
	else:
		client = FastTransport((BASTION_HOST, port))
	client.connect(username=LINUX_USER, password=LINUX_PWD)
	sftp = paramiko.SFTPClient.from_transport(client)
	print(REMOTE_QUERY_FILE)
	put_file(sftp,QUERY_FILE, REMOTE_QUERY_FILE)
	import stat
	put_file(sftp,PB_FILE, REMOTE_PB_FILE, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
	#e(0)
	stdout_data = []
	stderr_data = []
	session = client.open_channel(kind='session')

	session.settimeout(10)
	session.exec_command(command)
	while True:
		if session.recv_ready():
			data=session.recv(nbytes)
			print(data.decode("ascii"))
			
			if data.startswith(b'Java HotSpot(TM) 64-Bit Server VM warning:'):
				#print (123)
				break
			if session.recv_stderr_ready():
				stderr_data.append(session.recv_stderr(nbytes))
			if session.exit_status_ready():
				break
				

	with open(extract_to_file, 'ab') as the_file:
		while True:
			if session.recv_ready():
				data=session.recv(nbytes)
				#print('>%s<' % data.decode("ascii"))
				
				if not data.strip():
					print ('Ignoring newline.')
				else: #write first block
					the_file.write(data)
					#print('%d\tbytes written.' % len(data))
					total_bytes +=len(data)
					break
			if session.recv_stderr_ready():
				stderr_data.append(session.recv_stderr(nbytes))
			if session.exit_status_ready():
				break
		time1 = time.time()
		while True: #write the rest of the blocks
			if session.recv_ready():
				if 1:
					#print(session.recv(nbytes).decode("ascii"))
					data=session.recv(nbytes)
					the_file.write(data)
					#print('%d\tbytes written.' % len(data))
					total_bytes +=len(data)
				else:
					stdout_data.append(session.recv(nbytes))
			if session.recv_stderr_ready():
				stderr_data.append(session.recv_stderr(nbytes))
			if session.exit_status_ready():
				break
		time2 = time.time()
		print('TOTAL BYTES:\t%d' % total_bytes)
		print ('Elaplsed: %0.3f s' % ( (time2-time1)))
	print ('exit status: ', session.recv_exit_status())
	print(len(stdout_data))

	print (stderr_data)

	session.close()
	client.close()
	t_time2 = time.time()
	print ('TOTAL Elaplsed: %0.3f s' % ( (t_time2-t_time1)))
	
def get_tail(dump_file, n):
	with open(dump_file, 'rb') as f:
		assert n >= 0
		pos, lines = n+1, []
		while len(lines) <= n:
			try:
				f.seek(-pos, 2)
			except IOError:
				f.seek(0)
				break
			finally:
				lines = list(f)
			pos *= 2
	return lines[-n:]
	

def truncate_file(fh):
	fh.seek(0, os.SEEK_END)

	pos = fh.tell() - len(os.linesep.encode())
		
	while pos > 0 and fh.read(1) != "\n":
		pos -= 1
		fh.seek(pos, os.SEEK_SET)

	if pos > 0:
		fh.seek(pos+1, os.SEEK_SET)
		fh.truncate()
	
if __name__=='__main__':
	if 1:
		get_data(DATA_DUMP_FILE)
	if 1:
		tail=get_tail(DATA_DUMP_FILE, n=7 )
		tail.reverse()

		if 1:
			with open(DATA_DUMP_FILE, "r+", encoding = "utf-8") as fh:
				if 1:
					assert tail[0].endswith(b'logout'+os.linesep.encode()), "Wrong tail format (logout)"
					truncate_file(fh)
				if 1:
					assert tail[1].endswith(b'exit'+os.linesep.encode()), "Wrong tail format (exit)"
					truncate_file(fh)
				if 1:
					assert tail[2]==os.linesep.encode(), "Wrong tail format (new line)"
					truncate_file(fh)
				if 1:
					assert tail[3]==os.linesep.encode(), "Wrong tail format (new line)"
					truncate_file(fh)
				if 1:
					assert tail[4]==os.linesep.encode(), "Wrong tail format (new line)"
					truncate_file(fh)					
			
			
		
	