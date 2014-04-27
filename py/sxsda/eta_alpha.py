import sys
import os
import cPickle

#### eta / alpha ####

def get_eta(k,input_eta, voc_set, default = 0.01):
    eta = {}
    for voc in voc_set:
        if not voc in input_eta:
            eta[voc] = [default for x in xrange(k)]
        else:
            eta[voc] = input_eta[voc]
    
    return eta
            
def write_eta(eta,path):
    cPickle.dump(eta,open(path,'w'))

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
                
