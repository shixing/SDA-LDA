from multiprocessing import Process, Queue, Lock, Pool
import time
from functools import partial
import sxsda.eta_alpha as _mea


class ThreadSum:
    def __init__(self, value, lock):
        self.value = value
        self.lock = lock

    def get_value(self):
        value = None
        self.lock.acquire()
        value = self.value
        self.lock.release()
        return value

    def add_value(self,adder):
        self.lock.acquire()
        self.value += adder
        self.lock.release()


class LockedEta:
    def __init__(self,eta,lock):
        self.eta = eta
        self.lock = lock

    def get_eta(self,k,voc_set):
        self.lock.acquire()
        eta = _mea.get_eta(k,self.eta,voc_set)
        self.lock.release()
        return eta

    def write_eta(self,path):
        self.lock.acquire()
        _mea.write_eta(self.eta,path)
        self.lock.release()

    def add_eta(self,second):
        self.lock.acquire()
        _mea.add_eta(self.eta,second)
        self.lock.release()

    def get_eta_sum(self,k,V):
        self.lock.acquire()
        etaSum = _mea.get_eta_sum(self.eta,k,V)
        self.lock.release()
        return etaSum
                    
