import git, unittest, os, shutil

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
		
	def tearDown(self):
		shutil.rmtree('temp')
	
class TestMethodsError(unittest.TestCase):
	pass
	
if __name__ == '__main__':
	unittest.main()
