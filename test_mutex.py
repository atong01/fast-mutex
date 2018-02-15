import unittest
from mutex import FastMutexAlgorithm


class TestFastMutexAlgorithm(unittest.TestCase):
    def setUp(self):
        self.n = 100
        self.a = FastMutexAlgorithm(self.n)

    def test_state_sets(self):
        def get_lengths():
            return list(map(len, self.a.get_state_sets()))

        def verify_set_pair(a,b):
            """ Verifys a pair of state sets """
            self.assertEqual(sum(map(len, a)), self.n)
            self.assertEqual(sum(map(len, b)), self.n)
            self.assertLessEqual(tuple(map(len, a))[-1], 1)
            self.assertLessEqual(tuple(map(len, b))[-1], 1)

        self.assertEqual(get_lengths(), [100, 0, 0, 0])
        self.a.start(self.n)
        self.assertEqual(get_lengths(), [0, 0, 100, 0])
        last_state = self.a.get_state_sets()
        for i in range(100000):
            self.a.transition()
            next_state = self.a.get_state_sets()
            print("{}".format(get_lengths()))
            verify_set_pair(last_state, next_state)
            last_state = next_state
            if i % self.n == 0:
                print("{}".format(get_lengths()))
            if len(self.a.quiet) == self.n:
                return

if __name__ == '__main__':
    unittest.main()

