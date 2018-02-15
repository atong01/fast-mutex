import unittest
import scheduler as sch

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.n = 100

    def test_krrrandom_k_equals_n(self):
        """ This test is meant to verify the round property of the KRRR
        shuffler.
        """
        self.scheduler = sch.KRRRandomScheduler(range(self.n), k = None)
        for i in range(200 * self.n):
            self.scheduler.schedule()
        for i in range(200):
            self.assertEqual(len(set(self.scheduler.history[self.n*i: self.n * (i + 1)])), 100)

    def test_krrrandom_k_less_than_n(self):
        """ This test is meant to verify the round property of the KRRR
        shuffler.
        """
        k = int(self.n/2)
        self.scheduler = sch.KRRRandomScheduler(range(self.n), k = k)
        for i in range(200 * k):
            self.scheduler.schedule()
        for i in range(200):
            self.assertEqual(len(set(self.scheduler.history[k*i: k*(i+1)])), k)

    def test_single(self):
        """ Asserts that the single scheduler only runs proc 0 """
        self.scheduler = sch.SingleScheduler(range(self.n))
        for i in range(200):
            self.scheduler.schedule()
        self.assertEqual(self.scheduler.history, [0] * 200)

    def test_round_robin_k_equals_n(self):
        self.scheduler = sch.KRoundRobinScheduler(range(self.n), k = None)
        for i in range(200 * self.n):
            self.scheduler.schedule()
        for i in range(200):
            self.assertEqual(self.scheduler.history[self.n*i: self.n * (i + 1)],
                             [i for i in range(self.n)])

    def test_round_robin_k_less_than_n(self):
        k = int(self.n/2)
        self.scheduler = sch.KRoundRobinScheduler(range(self.n), k = k)
        for i in range(200 * k):
            self.scheduler.schedule()
        for i in range(200):
            self.assertEqual(self.scheduler.history[k*i: k* (i + 1)],
                             [i for i in range(k)])

if __name__ == '__main__':
    unittest.main()
