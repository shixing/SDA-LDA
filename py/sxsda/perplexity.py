import numpy as np
import math

def perplexity(test_trainW, test_testW, alpha, lamb, etaSum):  
  k = len(alpha)
  numDoc = len(test_testW)
  gammaList = []
  
  # Calculate gamma values
  for i in xrange(numDoc):
    gamma = localVB(test_trainW[i], alpha, lamb, k, etaSum)
    gammaList.append(gamma)
  
  # Calculate perplexity
  nume = 0.
  deno = 0.  
  for i in xrange(numDoc):
    doc = test_testW[i]
    
    for (wordID, count) in doc:
      nume = nume + logPW(wordID, gamma[i], lamb)
      deno = deno + count
      
  return nume / deno 
    
def localVB(doc, alpha, lamb, k, etaSum):
  # Global Variables
  VAR_MAX_ITER = 1000
  VAR_CONVERGED = 0.001
  
  # Initialization
  gamma = np.asarray([1.0 / k for i in xrange(k)])
  phi = {}
  
  for round in xrange(VAR_MAX_ITER):
    # E_q[log theta] & E_q[log beta]
    ElogTheta = psi(gamma)
    ElogBeta = elogBeta(lamb, etaSum)
    
    # Update phi
    for wordID in lamb:  
      phi[wordID] = np.exp(ElogTheta + ElogBeta[wordID])
      phi[wordID] = phi[wordID] / sum(phi[wordID])
    
    # Update gamma
    lastgamma = gamma
    gamma = alpha + phiTimeWordCount(doc, phi, k)
    
    # isConverged ?
    meanchange = np.mean(abs(gamma - lastgamma))
    if (meanchange < VAR_CONVERGED):
      break
      
  return gamma
  
def phiTimeWordCount(doc, phi, k):
  sum = np.asarray([0 for i in xrange(k)])
  
  for (wordID, count) in doc:
    sum = sum + phi[wordID] * count
  
  return sum
          
def elogBeta(lamb, etaSum):
    """
    E_q [log(beta) | lambda]
    """
    k = len(etaSum)
    ElogBeta = {}
    # Evaluate the second term of ElogBeta  
    for wordID in lamb:
      ElogBeta[wordID] = psi(lamb[wordID]) - psi(etaSum)
    
    return ElogBeta    
  
def logPW(wordID, gamma, lamb):
  k = len(gamma)
  lambOfWord = lamb[wordID]
  
  term = 0
  for i in xrange(k):
    term = term + (gamma[i] / sum(gamma)) * (lambOfWord[i] / sum(lambOfWord))
    
  return log(term)
  
if __name__ == '__main__':
  main()
