import sys
import os
import cPickle
import random


#### eta / alpha ####

def get_eta(k,input_eta, voc_set, default=None):
    eta = {}
    for voc in voc_set:
        if not voc in input_eta:
            # random init eta, otherwise will be equal distributed on eta
            eta[voc] = [0.01+random.random()/100 for x in xrange(k)]
        else:
            eta[voc] = input_eta[voc]
    
    return eta
            
def write_eta(eta,path,bPickle=False):
    if bPickle:
        cPickle.dump(eta,open(path,'w'))
    else:
        cPickle.dump(eta,open(path,'w')) 
        output = open(path+'.txt','w')
        for wid in eta:
            value_str = ', '.join(['%.6f' % x for x in eta[wid]])
            s = 'WID:{} [{}]\n'.format(wid,value_str)
            output.write(s)
        output.close()


def load_eta(path):
    eta = cPickle.load(open(path))
    return eta
    
def get_alpha(k):
    alpha = [1.0/k for x in xrange(k)]
    return alpha

def add_eta(first,second):
    for key2 in second:
        if not key2 in first:
            first[key2] = [0.01] * len(second[key2])
        for i in xrange(len(second[key2])):
            first[key2][i] += second[key2][i]
    
    return first
                
def get_eta_sum(eta,k,V,default = 0.01):
    partSum = default * (V-len(eta))
    etaSum = [partSum]*k
    for wid in eta:
        for i in xrange(k):
            etaSum[i] += eta[wid][i]
    return etaSum
    
