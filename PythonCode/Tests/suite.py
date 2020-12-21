import unittest


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
