import os, argparse

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
	os.mkdir(repo)
	os.mkdir(os.path.join(repo, '.git'))
	for name in ['objects', 'refs', 'refs/heads']:
		os.mkdir(os.path.join(repo, '.git', name))
	write_file(os.path.join(repo,'.git', 'HEAD'),
			   b'ref: refs/heads/master')
	print('initialized empty repository: {}'.format(repo))
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	sub_parsers = parser.add_subparsers(dest='command', metavar='command')
	sub_parsers.required = True
	
	# git-python init
	subparser = sub_parsers.add_parser('init', help='initialize a new repo')
	subparser.add_argument('repo', help='directory name for new repo')
	
	args = parser.parse_args()
	if args.command == 'init':
		init(args.repo)


