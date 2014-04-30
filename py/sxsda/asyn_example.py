from multiprocessing import Process, Queue, Lock, Pool
import time
from functools import partial

class ThreadSum:
    def __init__(self, value, lock,p):
        self.value = value
        self.lock = lock
        self.p = p

    def get_value(self):
        value = None
        self.lock.acquire()
        value = self.value
        self.lock.release()
        return value

    def add_value(self,value):
        self.lock.acquire()
        self.value += value
        if self.p:
            print 'value:', self.value
        self.lock.release()

def mycallback(adder,threadsum,ntsum):
    threadsum.add_value(adder)
    ntsum.add_value(-1)
    

def worker(x):
    time.sleep(1)
    print ':',x
    return x

def main():
    n=4
    tsum = ThreadSum(1,Lock(),True)
    ntsum = ThreadSum(0,Lock(),False)
    pool = Pool(processes = n)
    rs = []
    for i in xrange(10):
        while True:
            if ntsum.get_value() < n:
                break
        mcb = lambda x : mycallback(x,tsum,ntsum)
        value = tsum.get_value()
        print '*',value,'*'
        ntsum.add_value(1)
        result = pool.apply_async(worker,(value,),callback=mcb)
        rs.append(result)
    for i,r in enumerate(rs):
        r.wait()
        
main()
