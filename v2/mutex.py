"""
Implements potential low space low RMR mutex algorithm

Input n processes.
Model:
    Oblivious adversary

"""

from math import ceil, log
import logging
import numpy as np
from enum import Enum
from random import Random

DEBUG = True

class Randomizer(object):
    def __init__(self, n, seed = None):
        """ The randomizer must know n to produce the correct distribution """
        self.seed = 42 if DEBUG else seed
        self.random = Random(self.seed)
        self.n = n
        self.logn = int(ceil(log(n,2)))

    def flip(self):
        return self.random.randint(0,1) == 1 

    def geometric(self):
        """ Implements a clipped geometric distribution """
        val = np.random.geometric(p=0.5)
        if val >= self.logn:
            val = self.logn - 1
        return val

class PState(Enum):
    QUIET = 0
    SPIN = 1
    SEEK = 2
    CRIT = 3

class Process(object):
    """ The process class.

    The 

    """
    def __init__(self, name, rand, num_gadgets, reg_per_gadget):
        self.name = name
        self.state = PState.QUIET
        self.loc = 0
        self.rand = rand
        self.num_gadgets = num_gadgets
        self.reg_per_gadget = reg_per_gadget
        self.history = []

    def step(self):
        print("Process" + self.name + "step")
        if self.state == PState.QUIET:
            print("Quiet state no action")
        elif self.state == PState.SPIN:
            pass

    def flip(self):
        return self.random.randint(0,1) == 1

    def step(self, shared_mem):
        """ Step performs a process step."""
        s = self.state
        if s == PState.QUIET:
            return shared_mem, s
        if s == PState.SPIN:
            return shared_mem, s
        if s == PState.SEEK:
            return self.run_step(shared_mem), self.state
        if s == PState.CRIT:
            return self.exit_crit(shared_mem), self.state

    def run_step(self, shared_mem):
        toss = self.rand.flip()
        if toss:
            # Write
            index_to_write = self.rand.geometric(p=0.5)
            shared_mem[self.loc, index_to_write] = 1
            self.loc += 1
            if loc == self.num_gadgets:
                # We enter the critical section
                self.state = PState.CRIT
        else:
            # Wait
            for i in range(self.reg_per_gadget):
                if shared_mem[self.loc, i] == 1:
                    self.state == PState.SPIN


        print("ERROR run step not yet implemented")

    def exit_crit(self, shared_mem):
        print("ERROR exit crit not yet implemented")

    def __repr__(self):
        return "<Proc: {} State: {} Loc: {}>".format(
                self.name, self.state, self.loc)

    def __str__(self):
        return self.__repr__()


class FastMutexAlgorithm(object):
    def __init__(self, n, seed = None):
        """ Initializes the Fast Mutex Algorithm.

        The fast mutex algorithm has an array of log(n) gadgets each of depth 
        log(n). We maintain both a list of processes and a hash table containing
        a list of process ids spinning on each register.
        """
        self.rand = Randomizer(n, seed)

        self.n = n
        self.logn = int(ceil(log(n, 2)))
        self.mem  = np.zeros((self.logn, self.logn))
        self.writers = -1 * np.ones((self.logn, self.logn))
        self.spinners = {i : { j : [] for j in range(self.logn) }
                for i in range(self.logn)}
        self.proc_list = [Process(i, self.rand) for i in range(n)]
        self.schedule_history = []

    def schedule(self):
        """ Schedule processes obliviously """
        pnext = self.random.randrange(self.n)
        self.schedule_history.append(pnext)
        return self.proc_list[pnext]

    def transition(self):
        pnext = self.schedule()
        print("Transition: {}".format(pnext))
        self.mem, new_state = pnext.step(self, mem)
        if new_state == PState.SPIN:
            i,j =  pnext.loc
            self.spinners[i][j].append(pnext)

    def configuration(self):
        pass

if __name__ == '__main__':
    a = FastMutexAlgorithm(100)
    a.transition()
    






        
