import unittest

class TestRunner():
	def main(self):
		test_loader = unittest.defaultTestLoader
		suite = test_loader.discover("test")
		result = unittest.TestResult()
		suite.run(result)
		self.print_result(result)

	def print_result(self, result):
		for error in result.errors:
			print(error[1])
		print('Errors: {}\n'.format(result.errors))
		print('Failures: {}'.format(result.failures))

if __name__ == '__main__':
	TestRunner().main()