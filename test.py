import git, unittest, os, shutil, hashlib, zlib
from io import StringIO
from unittest.mock import patch

class BaseTestClass(unittest.TestCase):
		types = ['blob', 'commit', 'tree']
		hashes = ['e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
					   'dcf5b16e76cce7425d0beaef62d79a7d10fce1f5',
					   '4b825dc642cb6eb9a060e54bf8d69288fbee4904']
	
class TestInitSuccess(unittest.TestCase):

	def setUp(self):
		git.init('temp')
		
	def test_success(self):
		self.assertTrue(os.path.isdir('temp'))
		self.assertTrue(os.path.isdir('temp/.git'))
		self.assertTrue(os.path.isdir('temp/.git/objects'))
		self.assertTrue(os.path.isdir('temp/.git/refs'))
		self.assertTrue(os.path.isdir('temp/.git/refs/heads'))
		self.assertTrue(os.path.exists('temp/.git/HEAD'))
		self.assertEqual(git.read_file('temp/.git/HEAD'), b'ref: refs/heads/master')
		
	def tearDown(self):
		shutil.rmtree('temp')
	
class TestInitException(unittest.TestCase):
		
	def test(self):
		path = "TestInitException"
		os.mkdir(path)
		self.assertRaises(OSError, git.init, path)
		os.rmdir(path)

class TestHashSuccess(BaseTestClass):

	def setUp(self):
		git.init('temp')

	def testHashing(self):
		for i in range(len(self.types)):
			self.assertEqual(git.hash_object(b'',self.types[i],False), self.hashes[i])


	def testWritingToFiles(self):
		for i in range(len(self.types)):
			git.hash_object(b'',self.types[i],True)
			path = os.path.join('.git', 'objects', self.hashes[i][:2], self.hashes[i][2:])
			self.assertTrue(os.path.exists(path))
			self.assertEqual(git.read_file(path), 
							 zlib.compress((self.types[i] + ' 0\x00').encode()))
		
	def tearDown(self):
		shutil.rmtree('temp')
		
#class TestFindObjectSuccess(unittest.TestCase):
#	def setUp(self):
#		git.init('temp')
#		# hash with no data of type 'blob', type 'commit', type 'tree' respectively	
#		self.types = ['blob', 'commit', 'tree']
#		self.hashes = ['e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
#					   'dcf5b16e76cce7425d0beaef62d79a7d10fce1f5',
#					   '4b825dc642cb6eb9a060e54bf8d69288fbee4904']
#	
#	# TODO: why does not fail if objects not previously hashed?				   
#	def testFindObjects(self):
#		for sha1 in self.hashes:
#			path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
#			self.assertEqual(path, git.find_object(sha1))
#		
#	def tearDown(self):
#		shutil.rmtree('temp')

class TesFindObjectException(unittest.TestCase):
	def testFindObjectLenException(self):
		self.assertRaises(ValueError, git.find_object, '')
		self.assertRaises(ValueError, git.find_object, 'a')
	
	def testFindObjectNoFolderException(self):
		self.assertRaises(ValueError, git.find_object, 'abcd')
		
class TestReadObjectSuccess(BaseTestClass):
	def setUp(self):
		git.init('temp')
			
		for i in range(len(self.types)):
			git.hash_object(b'',self.types[i],True)
					   
	def testReadObjects(self):
		for i in range(len(self.types)):
			self.assertEqual((self.types[i], b''), git.read_object(self.hashes[i]))
		
	def tearDown(self):
		shutil.rmtree('temp')

class TestCatFileSuccess(BaseTestClass):
	def setUp(self):
		git.init('temp')
	
	def testSuccess(self):
		with patch('sys.stdout', new = StringIO()) as stdout:
			sha1 = git.hash_object(b'123', 'blob', True)
			
			# test obj_type = 'blob'
			git.cat_file('blob', sha1)
			self.assertEqual(stdout.getvalue().strip(), "b'123'")
			# since getValue reads all printed content, seek to beginning to overwrite
			stdout.seek(0)
			stdout.truncate(0)
			
			# test 'size'
			git.cat_file('size', sha1)
			self.assertEqual(stdout.getvalue().strip(), "3")
			stdout.seek(0)
			stdout.truncate(0)
			
			# test 'type'
			git.cat_file('type', sha1)
			self.assertEqual(stdout.getvalue().strip(), "blob")
			stdout.seek(0)
			stdout.truncate(0)
			
			# test 'pretty'
			git.cat_file('pretty', sha1)
			self.assertEqual(stdout.getvalue().strip(), "b'123'")
			stdout.seek(0)
			stdout.truncate(0)			

			# TODO: test 'pretty' for 'tree'
			
	def tearDown(self):
		shutil.rmtree('temp')
		
		
if __name__ == '__main__':
	unittest.main()
