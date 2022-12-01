import os, argparse, hashlib, zlib, collections, enum


# Data for one entry in the git index (.git/index)
IndexEntry = collections.namedtuple('IndexEntry', [
	'ctime_s', 'ctime_n', 'mtime_s', 'mtime_n', 'dev', 'ino', 'mode', 'uid',
	'gid', 'size', 'sha1', 'flags', 'path',
])

class objectType(enum.Enum):
	"""Object type enum. There are more types which have not been included.
	"""
	commit = 1
	tree = 2
	blob = 3
	
def read_file(path):
	"""Read contents of file at given path as bytes."""
	with open(path, 'rb') as f:
		return f.read()
		
def write_file(path, data):
	"""Write data bytes to file at given path."""
	with open(path, 'wb') as f:
		f.write(data)
		
def init(repo):
	"""Create directory for repo and initialize .git directory."""
	try:
		os.mkdir(repo)
		os.mkdir(os.path.join(repo, '.git'))
		for name in ['objects', 'refs', 'refs/heads']:
			os.mkdir(os.path.join(repo, '.git', name))
		write_file(os.path.join(repo,'.git', 'HEAD'),
				   b'ref: refs/heads/master')
	except OSError as error:
		print(error)
		raise
	else:
		print('initialized empty repository: {}'.format(repo))
		
def hash_object(data, obj_type, write=True):
	"""Compute hash of object data of given type and write to object store
	if "write" is True. Return SHA-1 object hash as hex string.
	"""
	header = '{} {}'.format(obj_type, len(data)).encode()
	full_data = header + b'\x00' + data
	sha1 = hashlib.sha1(full_data).hexdigest()
	if write:
		path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
		if not os.path.exists(path):
			os.makedirs(os.path.dirname(path), exist_ok=True)
			write_file(path, zlib.compress(full_data))
	return sha1
	
if __name__ == '__main__': # pragma: no cover
	parser = argparse.ArgumentParser() 
	sub_parsers = parser.add_subparsers(dest='command', metavar='command')
	sub_parsers.required = True
	
	# git init
	subparser = sub_parsers.add_parser('init', help='initialize a new repo')
	subparser.add_argument('repo', help='directory name for new repo')
	
	args = parser.parse_args()
	if args.command == 'init':
		init(args.repo)


