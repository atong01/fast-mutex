class SharedMemoryBase(object):
    """ Inits a shared memory consisting of a dictionary of registers """
    def __init__(self, registers = None):
        if registers is None:
            registers = {}
        self.registers = registers

    def get(addr, pname = None):
        return self.registers[addr]

class RWMemory(SharedMemoryBase):
    def __init__(self, registers = None):
        super().__init__(registers)

    def read(addr, pname = None):
        return self.registers[addr].read()
    
    def write(addr, value, pname = None)
        return self.registers[addr].write(value)
