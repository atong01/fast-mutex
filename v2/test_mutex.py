import unittest
from mutex import FastMutexAlgorithm

class TestFastMutexAlgorithm(unittest.TestCase):
    def setUp(self):
        pass

    def test_logn(self):
        a = FastMutexAlgorithm(100)
        print (a.n, a.logn)

if __name__ == '__main__':
    unittest.main()


