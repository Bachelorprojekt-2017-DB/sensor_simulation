import unittest
import coverage
import sys

class TestRunner():
	def main(self):
		test_loader = unittest.defaultTestLoader
		suite = test_loader.discover("test")
		result = unittest.TestResult()
		suite.run(result)
		self.print_result(result)
		if not result.wasSuccessful():
			sys.exit("Test failure")

	def print_result(self, result):
		print('Errors:')
		for error in result.errors:
			print(error[0])
			print(error[1])
		print('Failures:')
		for failure in result.failures:
			print(failure[0])
			print(failure[1])

if __name__ == '__main__':
	cov = coverage.Coverage()
	cov.start()
	TestRunner().main()
	cov.stop()
	cov.save()
	cov.html_report()
