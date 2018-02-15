"""
Implements potential low space low RMR mutex algorithm.

Notes:
This algorithm doesn't actually perform mutual exclusion as the number of
processes in the critical section is not enforced. This is fixable with an
additional deterministic exclusion step.
"""

from math import ceil, log
from enum import Enum
import numpy as np

from scheduler import *
from randomizer import Randomizer


class PState(Enum):
    QUIET = 0
    SPIN = 1
    SEEK = 2
    CRIT = 3

class Process(object):
    """ The process class.
    
    The transition diagram for a process
    QUIET --> SEEK --> CRIT --> QUIET
               ||
              SPIN
    """
    def __init__(self, name, rand, num_gadgets, reg_per_gadget):
        self.name = name
        self.state = PState.QUIET
        self.loc = 0
        self.rand = rand
        self.spin_loc = None
        self.num_gadgets = num_gadgets
        self.reg_per_gadget = reg_per_gadget
        self.history = []

    def step(self, shared_mem):
        """ Step performs a process step."""
        s = self.state
        if s == PState.QUIET:
            pass
        if s == PState.SPIN:
            if shared_mem[self.spin_loc] == -1:
                # REVIEW (atong): This waking does not check registers of
                # Higher index.
                #print("Waking Proc: {}".format(self.name))
                self.state = PState.SEEK
                self.spin_loc = None
        if s == PState.SEEK:
            shared_mem = self.run_step(shared_mem)
        if s == PState.CRIT:
            shared_mem = self.exit_crit(shared_mem)
        return shared_mem, self.state

    def run_step(self, shared_mem):
        toss = self.rand.flip()
        if toss:
            # Write
            index_to_write = self.rand.geometric(self.reg_per_gadget)
            #print("Writing to ({},{})".format(self.loc, index_to_write))
            shared_mem[self.loc, index_to_write] = self.name
            self.loc += 1
            if self.loc == self.num_gadgets:
                # We enter the critical section
                self.state = PState.CRIT
            #print (shared_mem)
        else:
            # Wait
            for i in range(self.reg_per_gadget):
                if shared_mem[self.loc, i] > -1:
                    #print("Waiting on ({},{})".format(self.loc, i))
                    self.state = PState.SPIN
                    self.spin_loc = (self.loc, i)
                    break
        return shared_mem

    def exit_crit(self, shared_mem):
        """ Iterate backward over each gadget, if this process was the last one
        to write to the register then reset all registers in that gadget.
        """
        for i in reversed(range(self.num_gadgets)):
            do_reset_i = False
            for j in range(self.reg_per_gadget):
                if shared_mem[i,j] > -1 and shared_mem[i,j] == self.name:
                    do_reset_i = True
                    break
            if not do_reset_i:
                continue
            #print("Proc: {} resetting gadget {}".format(self.name, i))
            for j in range(self.reg_per_gadget):
                shared_mem[i,j] = -1

        self.state = PState.QUIET
        self.loc   = 0
        return shared_mem

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

        self.n        = n
        self.logn     = int(ceil(log(n, 2)))
        self.gadgets  = 2 * self.logn
        self.reg_per_gadget = self.logn
        self.mem      = -1 * np.ones((self.gadgets, self.reg_per_gadget))
        self.writers  = -1 * np.ones((self.gadgets, self.reg_per_gadget))
        self.spinners = {i : { j : [] for j in range(self.reg_per_gadget) }
                for i in range(self.gadgets)}
        self.proc_list = [Process(i, self.rand, self.gadgets, self.reg_per_gadget) for i in range(n)]

        #self.scheduler = SingleScheduler(self.proc_list, k = None)
        #self.scheduler = KRoundRobinScheduler(self.proc_list, k = None)
        self.scheduler = KRRRandomScheduler(self.proc_list, k = None)

        self.quiet = set(self.proc_list)
        self.spin = set()
        self.seek = set()
        self.crit = set()
        self.rmr = 0

    def start(self, k):
        """ K quiet processes to SEEK state """
        to_start = min(k, len(self.quiet))
        print ("Starting {} processes".format(to_start))
        for i in range(to_start):
            p = self.quiet.pop()
            p.state = PState.SEEK
            self.seek.add(p)

    def transition(self):
        pnext = self.scheduler.schedule()
        os = pnext.state
        self.mem, ns = pnext.step(self.mem)
        #print("Transition: {} to {}".format(pnext, new_state))
        if os == PState.SEEK and ns == PState.SPIN:
            i,j =  pnext.spin_loc
            self.spinners[i][j].append(pnext)
            self.seek.remove(pnext)
            self.spin.add(pnext)
        if os == PState.SPIN and ns == PState.SEEK:
            self.spin.remove(pnext)
            self.seek.add(pnext)
        if os == PState.SEEK and ns == PState.CRIT:
            self.seek.remove(pnext)
            self.crit.add(pnext)
            if len(self.crit) > 1:
                #print("ERROR: multiple processes in critical section")
                pass
        if os == PState.CRIT and ns == PState.QUIET:
            self.crit.remove(pnext)
            self.quiet.add(pnext)
            #print("Quiet set ".format(self.quiet))
        if os == PState.SPIN and ns == PState.SPIN:
            self.rmr += 0
        else:
            self.rmr += 1

    def get_state_sets(self):
        return self.quiet, self.spin, self.seek, self.crit

    def run(self, outfile, k = None):
        if k is None:
            k = self.n
        self.start(k)
        f = outfile
        for i in range (100000000):
            self.transition()
            if len(self.quiet) == k:
                print("Stopping after {} transitions, {} rounds, total rmr = {}, rmr per crit {}".format(i, i // k, self.rmr, self.rmr / self.n))
                f.write('{},{},{},{}\n'.format(k, i // k, self.rmr, self.rmr / k))
                return

def interactive_main():
    #n = input("How many processes would you like?")
    n = 10
    a = FastMutexAlgorithm(n)
    a.start(n)
    while True:
        contine_run = input("Step? ")
        a.transition()

def main():
    f = open('results.csv', 'w')
    f.write("Number of Processes, Number of Rounds, Total RMR, RMR per Critical Section\n")
    for i in range(100, 2000, 25):
        for j in range(10):
            a = FastMutexAlgorithm(i)
            a.run(f)

if __name__ == '__main__':
    main()
    #interactive_main()
