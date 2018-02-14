class RegisterBase(object):
    def __init__(self, value):
        self._value = value

class RWRegister(RegisterBase):
    def __init__(self, value):
        super(RWRegister, self).__init__(value)
        self._last_writer = None
        self._writer_history = []

    def read(self):
        return self._value

    def write(self, value, pname = None):
        self._value = value
        self._last_writer = pname
        self._writer_history.append(pname)

    def get_writer(self):
        return self._last_writer

class RORegister(RegisterBase):
    def __init__(self, value):
        super(RORegister, self).__init__(value)

    def read(self):
        return self._value
    
class RWBit(RWRegister):
    """ RW bit register
    """
    def __init__(self, value = 0):
        self.valid_set = set([0,1])
        if value not in self.valid_set:
            raise ValueError("RWBit set to non bit value")
        super(RWBit, self).__init__(value)


