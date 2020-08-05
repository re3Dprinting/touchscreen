from PyQt5.QtCore import QObject, pyqtSignal

class Ctor(QObject):

    # PyQt signals have to be created here. The QObject constructor
    # will bind them to local names.
    signal = pyqtSignal(str, str)

    def __init__(self):
        super(Ctor, self).__init__()

    def register(self, slot):
        self.signal.connect(slot)

    def notify(self, from_state, to_state):
        self.signal.emit(from_state, to_state)
    
class CtorStr(QObject):
    signal = pyqtSignal(str)

    def __init__(self):
        super(CtorStr, self).__init__()

    def register(self, slot):
        self.signal.connect(slot)

    def notify(self, value):
        self.signal.emit(value)

class CtorDict(QObject):
    signal = pyqtSignal(dict)

    def __init__(self):
        super(CtorDict, self).__init__()

    def register(self, slot):
        self.signal.connect(slot)

    def notify(self, dict):
        self.signal.emit(dict)

class CtorTuple(QObject):
    signal = pyqtSignal(tuple)

    def __init__(self):
        super(CtorTuple, self).__init__()

    def register(self, slot):
        self.signal.connect(slot)

    def notify(self, tuple):
        self.signal.emit(tuple)
