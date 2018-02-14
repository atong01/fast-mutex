from random import Random
from math import ceil, log
from register import RWBit
from memory import RWMemory
import pprint

DEBUG = True
DEBUG_SEED = 42

class Schedule(object):
    """ Initialize a process schedule.
    Args:
        n: (int) number of processes
        stype: (str) string representing how to generate schedule

    OBL type is an oblivious adversary, each process is scheduled chosen
    with replacement.
    SIN type is a process 0 only schedule

    """
    def __init__(self, n, stype = "OBL", seed = None):
        self.history = []
        self.num_p   = n
        self.stype   = stype
        if DEBUG:
            seed = 42
        self.random = Random(seed)

    def next(self):
        if self.stype == "OBL":
            next_p = self.random.randint(0, self.num_p - 1)
        if self.stype == "SIN":
            next_p = 0
        self.history.append(next_p)
        return next_p

    def next_n(self, length):
        return [self.next() for i in range(length)]

class Flipper(object):
    """ Initializes a flipper object, this holds the history of all coin flips.
    """
    def __init__(self, seed):
        self.history = []
        if DEBUG:
            seed = 42
        self.random = Random(seed)

    def next(self):
        flip = self.random.randint(0,1)
        self.history.append(flip)
        return flip

    def next_n(self, length):
        return [self.next() for i in range(length)]


class Process(object):
    """ Initialize a process with an associated shared memory object """
    def __init__(self, name, sm):
        self.flipper = Flipper()
        self.name = name
        self.sm = sm
    
    def step():
        pass

class Gadget(object):
    def __init__(self, name, size):
        self.name = name
        self.registers = [RWBit() for i in range(size)]

class FastMutexMemory(RWMemory):
    def __init__(self, n):
        super(FastMutexMemory, self).__init__()
        self.n = n
        self.num_gadgets = int(ceil(log(self.n)))
        self.num_reg_per_gadget = int(ceil(log(self.n)))
        for gadget in range(self.num_gadgets):
            for reg in range(self.num_reg_per_gadget):
                self.registers[(gadget, reg)] = RWBit()


    def matrix_map(self, f):
        """ map function f applied to each register to a matrix.
        """
        mat = []
        for gadget in range(self.num_gadgets):
            gadget = []
            for reg in range(self.num_reg_per_gadget):
                gadget.append(self.registers[(gadget, reg)].f())
            mat.append(gadget)
        return mat

    def get_state_matrix(self):
        return self.matrix_map(read)

    def get_writer_matrix(self):

    
    def __repr__(self):
        return "FastMutexAlgorithmMemory"
    
    def __str__(self):
        s = ""
        for gadget in range(self.num_gadgets):
            for reg in range(self.num_reg_per_gadget):
                s += str(self.registers[(gadget, reg)].read())
            s += "\n"
        return s


class FastMutexAlgorithm(object):
    def __init__(self, n):
        self.n = n
        self.schedule = Schedule(n, stype = "OBL")
        self.sm = FastMutexMemory(n)


if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)
    alg = FastMutexAlgorithm(100)
    print (alg.sm)



