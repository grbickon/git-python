import git, unittest, os, shutil, hashlib, zlib

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

class TestHashObjectSuccess(unittest.TestCase):

	def setUp(self):
		git.init('temp')
		
	def testEmptyBlob(self):
		# no data, type 'blob'
		sha1 = 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391'
		self.assertEqual(git.hash_object(b'','blob',True), sha1)
		path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
		self.assertTrue(os.path.exists(path))
		self.assertEqual(git.read_file(path), zlib.compress(b'blob 0\x00'))

	def tearDown(self):
		shutil.rmtree('temp')
	
if __name__ == '__main__':
	unittest.main()
