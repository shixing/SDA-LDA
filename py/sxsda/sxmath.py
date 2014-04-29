import numpy as np
from scipy.misc import logsumexp

def mylogsumexp(a):
    assert(a.size>=2)
    s = logsumexp(a[0:2])
    for i in xrange(2,a.size):
        s = logsumexp([s,a[i]])
    return s

def test_mylogsumexp():
    a = np.asarray([1,2,5])
    print logsumexp(a)
    print mylogsumexp(a)

def test_digamma():
    print digamma(0.1)


def digamma(x):
    x=x+6
    p=1.0/(x*x)
    p=(((0.004166666666667*p-0.003968253986254)*p+0.008333333333333)*p-0.083333333333333)*p
    p=p+np.log(x)-0.5/x-1/(x-1)-1/(x-2)-1/(x-3)-1/(x-4)-1/(x-5)-1/(x-6)
    return p



if __name__ == '__main__':
    test_digamma()
