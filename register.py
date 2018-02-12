class RegisterBase(object):
    def __init__(self, value):
        self.value = value

class RWRegister(RegisterBase):
    def __init__(self, value):
        super().__init__(value)

    def read(self):
        return self.value

    def write(self, value):
        self.value = value

class RORegister(RegisterBase):
    def __init__(self, value):
        super().__init__(value)

    def read(self):
        return self.value
    
class RWBit(RWRegister):
    """ RW bit register
    """
    def __init__(self, value = 0):
        self.valid_set = set([0,1])
        if value not in self.valid_set:
            raise ValueError("RWBit set to non bit value")
        super().__init__(value)


