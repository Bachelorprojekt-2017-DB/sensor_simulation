import unittest
import coverage

class TestRunner():
	def main(self):
		cov = coverage.Coverage()
		cov.start()
		test_loader = unittest.defaultTestLoader
		suite = test_loader.discover("test")
		result = unittest.TestResult()
		suite.run(result)
		self.print_result(result)
		cov.stop()
		cov.save()
		cov.html_report()

	def print_result(self, result):
		for error in result.errors:
			print(error[1])
		print('Errors: {}\n'.format(result.errors))
		print('Failures: {}'.format(result.failures))

if __name__ == '__main__':
	TestRunner().main()