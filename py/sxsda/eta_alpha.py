import sys
import os
import cPickle
import random
import gensim

#### eta / alpha ####

def get_eta(k,input_eta, voc_set, default=None):
    eta = {}
    for voc in voc_set:
        if not voc in input_eta:
            # random init eta, otherwise will be equal distributed on eta
            eta[voc] = [1.0/k+random.random()/100 for x in xrange(k)]
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


def get_gensim_eta_etaSum(fname,voc_set):
  ldaModel = gensim.models.ldamodel.LdaModel.load(fname)
  lamb = ldaModel.state.get_lambda()
  
  # Number of words
  numWords = len(lamb[0])
  # Number of topics
  numTopics = len(lamb)

  print numTopics
  print numWords

  lambMap = {}
  for voc in voc_set:
      temp = []
      for k in xrange(numTopics):
          temp.append(lamb[k][voc])
      lambMap[voc] = temp

  etaSum = []
  for k in xrange(numTopics):
      etaSum.append(sum(lamb[k]))



  return lambMap,etaSum



def load_eta(path):
    eta = cPickle.load(open(path))
    return eta
    
def get_alpha(k):
    alpha = [1.0/k for x in xrange(k)]
    return alpha

def add_eta(first,second):
    for key2 in second:
        if not key2 in first:
            first[key2] = [1.0/len(second[key2])] * len(second[key2])
        for i in xrange(len(second[key2])):
            first[key2][i] += second[key2][i]
    
    return first
                
def get_eta_sum(eta,k,V):
    default = 1.0/k
    partSum = default * (V-len(eta))
    etaSum = [partSum]*k
    for wid in eta:
        for i in xrange(k):
            etaSum[i] += eta[wid][i]
    return etaSum
    
