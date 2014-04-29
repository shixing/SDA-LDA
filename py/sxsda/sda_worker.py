import numpy as np
from scipy.special import psi
from scipy.special import gamma as gammaFu
from scipy.special import polygamma
from scipy.misc import logsumexp
from sxsda.sxmath import mylogsumexp

np.seterr(invalid='raise')

def main():
  doc1 = [(1,1), (2,1)]
  doc2 = [(1,5), (2,1)]
  
  miniBatch = [doc1, doc2]
  
  eta = {}
  eta[1] = [0.2, 0.2, 0.2, 0.2, 0.2]
  eta[2] = [0.2, 0.2, 0.2, 0.2, 0.2]
  etaSum = [1, 1, 1, 1, 1]
  
  alpha = [0.2, 0.2, 0.2, 0.2, 0.2]
  
  print lda_worker(miniBatch, eta, etaSum, alpha)
  
def lda_worker(miniBatch, eta, etaSum, alpha):
  # Global Variables
  VAR_MAX_ITER = 100
  VAR_CONVERGED = 0.001
 
  # Initialization
  k = len(alpha)
  alpha = np.asarray(alpha)
  etaArray = {}
  newLambda = {}
  etaSum = np.asarray(etaSum)
  
  # Convert eta to etaArray
  for wordID in eta:
    etaArray[wordID] = np.asarray(eta[wordID])
    newLambda[wordID] = np.asarray(eta[wordID])
  
  # Iterations
  globalDict = set()
  oldLambda = {};
  for round in xrange(VAR_MAX_ITER): 
    print round
    # Process each document
    term = {}
    for doc in miniBatch:  
      phi = localVB(doc, alpha, newLambda, k, etaSum)
    
    # test 
    # for wordID in phi:  
    #   print sum(phi[wordID]) 
      
      # Calculate the summation terms
      for (wordID, count) in doc:
        globalDict.add(wordID)
        if not wordID in term :
          term[wordID] = count * phi[wordID]
        else:
          term[wordID] = term[wordID] + count * phi[wordID]
  
    oldLambda = newLambda
    newLambda = {}
    for wordID in globalDict:
      newLambda[wordID] = etaArray[wordID] + term[wordID]
    
    # Update etaSum
    deltaEtaSum = np.asarray([0 for i in xrange(k)])
    for wordID in newLambda:
      deltaEtaSum = deltaEtaSum + (newLambda[wordID] - oldLambda[wordID])
    etaSum = etaSum + deltaEta
    
    # Converged?
    absDiff = np.asarray([0 for i in xrange(k)])
    
    for wordID in oldLambda:
      absDiff = absDiff + abs(oldLambda[wordID] - newLambda[wordID])
    
    meanchange = np.mean(absDiff)
    if (meanchange < VAR_CONVERGED):
      break
        
  # Delta lambda
  valReturn = {}
  for wordID in newLambda:
    valReturn[wordID] = (newLambda[wordID] - etaArray[wordID]).tolist()
  
  return valReturn
  
def localVB(doc, alpha, lamb, k, etaSum):
  # Global Variables
  VAR_MAX_ITER = 100
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
      phi[wordID] = ElogTheta + ElogBeta[wordID] # phi in log space
      try:
        phiLogSum = logsumexp(phi[wordID])
        phi[wordID] = np.exp(phi[wordID] - phiLogSum) # phi in normal space
      except Exception as e:
        print phi[wordID]
        print ElogTheta
        print ElogBeta[wordID]
        raise e
        
    
    # Update gamma
    lastgamma = gamma
    gamma = alpha + phiTimeWordCount(doc, phi, k)
    
    # isConverged ?
    meanchange = np.mean(abs(gamma - lastgamma))
    if (meanchange < VAR_CONVERGED):
      break
      
  return phi
    
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
      # edit by xingshi: lamb is probabliy going to be 0.0
      # and your final lamb will always convergy to some zero
      ElogBeta[wordID] = psi(lamb[wordID]+[0.0001]*k) - psi(etaSum)
      # for value in ElogBeta[wordID]:
      #   if value == float('inf'):
      #     print lamb[wordID]
      #     print etaSum
      #     break
    return ElogBeta  
  
if __name__ == '__main__':
  main()
