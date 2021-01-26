import unittest

def test_units():
    """
    Run smaller tests with unit in the name (run more often and quicker)
    :return:
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir='.', pattern='test_unit*.py')
    suite.addTests(tests)
    runner = unittest.TextTestRunner()
    runner.run(suite)
    
def test_suite():
    """
    Run all of the test cases in a test suite.
    :return:
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir='.',  pattern='test_*.py')
    suite.addTests(tests)
    runner = unittest.TextTestRunner()
    runner.run(suite)

if __name__ == '__main__':
    test_suite()
