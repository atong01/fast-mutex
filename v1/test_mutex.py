import unittest
from mutex import Schedule
from random import Random

class TestSchedule(unittest.TestCase):
    def setUp(self):
        self.random = Random(42)

    def test_sin(self):
        S = Schedule(1, stype = "SIN")
        for i in range(0,100):
            S.next()
        self.assertEqual(S.history, [0] * 100)

    def test_obl_seed(self):
        n = 200
        S = Schedule(n, stype = "OBL")
        for i in range(0,100):
            S.next()
        answer = [self.random.randint(0,n-1) for i in range(0,100)]
        self.assertEqual(S.history, answer)
        
if __name__ == '__main__':
    unittest.main()
