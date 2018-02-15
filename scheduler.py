from abc import ABC, abstractmethod
import randomizer

class Scheduler(ABC):
    def __init__(self, proc_list):
        self.proc_list = proc_list
        self.n = len(self.proc_list)
        self.history = []

    @abstractmethod
    def next_id(self):
        """ Returns integer x in range 0 <= x < n """
        pass

    def schedule(self):
        idnext = self.next_id()
        pnext = self.proc_list[idnext]
        self.history.append(idnext)
        return pnext

class SingleScheduler(Scheduler):
    def next_id(self):
        return 0

class KRoundRobinScheduler(Scheduler):
    def __init__(self, proc_list, k):
        super(KRoundRobinScheduler, self).__init__(proc_list)
        if k is None:
            k = self.n
        self.k = k
        self.last = -1

    def next_id(self):
        self.last = (self.last + 1) % self.k
        return self.last

class KRRRandomScheduler(Scheduler):
    def __init__(self, proc_list, k, seed = None):
        super(KRRRandomScheduler, self).__init__(proc_list)
        if k is None:
            k = self.n
        self.k = k
        self.rand = randomizer.Randomizer(self.n, seed)
        self.kset = set(range(k))
        self.futurep = set(range(k))

    def next_id(self):
        if len(self.futurep) == 0:
            self.futurep |= self.kset
        to_return = self.rand.random.choice(tuple(self.futurep))
        self.futurep.remove(to_return)
        return to_return

