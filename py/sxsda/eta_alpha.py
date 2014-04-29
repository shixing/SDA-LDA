import sys
import os
import cPickle
import random

#### eta / alpha ####

def get_eta(k,input_eta, voc_set, default = 0.01):
    eta = {}
    for voc in voc_set:
        if not voc in input_eta:
            eta[voc] = [default+random.random()/100 for x in xrange(k)]
        else:
            eta[voc] = input_eta[voc]
    
    return eta
            
def write_eta(eta,path,bPickle=False):
    if bPickle:
        cPickle.dump(eta,open(path,'w'))
    else:
        output = open(path+'.txt','w')
        for wid in eta:
            value_str = ', '.join(['%.3f' % x for x in eta[wid]])
            s = 'WID:{} [{}]\n'.format(wid,value_str)
            output.write(s)
        output.close()


def load_eta(path):
    eta = cPickle.load(open(path,'r'))
    return eta
    
def get_alpha(k):
    alpha = [1.0/k for x in xrange(k)]
    return alpha

def add_eta(first,second):
    for key2 in second:
        if key2 in first:
            for i in xrange(len(second[key2])):
                first[key2][i] += second[key2][i]
        else:
            first[key2] = second[key2]
    
    return first
                
def get_eta_sum(eta,k,V,default = 0.01):
    partSum = default * (V-len(eta))
    etaSum = [partSum]*k
    for wid in eta:
        for i in xrange(k):
            etaSum[i] += eta[wid][i]
    return etaSum
    
