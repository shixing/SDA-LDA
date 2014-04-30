import numpy as np
import math
from scipy.special import psi
from sxsda.sda_worker import localVB, phiTimeWordCount

def perplexity(test_trainW, test_testW, alpha, lamb, etaSum,debug = True):  
  k = len(alpha)
  numDoc = len(test_testW)
  gammaList = []
  
  # Calculate gamma values
  nConvergedDoc = 0
  for i in xrange(numDoc):
    phi,gamma, isConverged = localVB(test_trainW[i], alpha, lamb, k, etaSum)
    nConvergedDoc += 1
    gammaList.append(gamma)
    if debug:
      print 'Converged Doc:{}/{}'.format(nConvergedDoc,i+1)
  # Calculate perplexity
  nume = 0.
  deno = 0.  
  for i in xrange(numDoc):
    doc = test_testW[i]
    
    for (wordID, count) in doc:
      nume = nume + logPW(wordID, gammaList[i], lamb)
      deno = deno + count
      
  return nume / deno 
                
def logPW(wordID, gamma, lamb):
  k = len(gamma)
  lambOfWord = lamb[wordID]
  
  term = 0
  gammaSum = sum(gamma)
  lambOfWordSum = sum(lambOfWord)
  for i in xrange(k):
    term = term + (gamma[i] / gammaSum) * (lambOfWord[i] / lambOfWordSum)
    
  return np.log(term)
  
if __name__ == '__main__':
  main()
