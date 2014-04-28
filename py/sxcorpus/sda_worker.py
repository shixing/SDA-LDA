import numpy as np
from scipy.special import psi
from scipy.special import gamma as gammaFu
from scipy.special import polygamma

def main():
  doc = [(1,1), (2,2)]
  miniBatch = [doc, doc]
  
  eta = {}
  eta[1] = [0.2, 0.2, 0.2, 0.2, 0.2]
  eta[2] = [0.2, 0.2, 0.2, 0.2, 0.2]
  eta[3] = [0.2, 0.2, 0.2, 0.2, 0.2]
  
  alpha = [0.1, 0.1, 0.2, 0.3, 0.3]
  
  lda_worker(miniBatch, eta, alpha)
  
def lda_worker(miniBatch, eta, alpha):
  # Seed
  np.random.seed(100000001)
  # Global Variables
  VAR_MAX_ITER = 100
  VAR_CONVERGED = 0.001
 
  # Initialization
  k = len(alpha)
  v = 500000
  alpha = np.asarray(alpha)
  etaArray = {}
  newLambda = {}
  
  # Convert eta to etaArray
  for wordID in eta:
    etaArray[wordID] = np.asarray(eta[wordID])
    newLambda[wordID] = np.asarray(eta[wordID])
  
  # Iterations
  for round in xrange(VAR_MAX_ITER): 
    # Process each document
    for doc in miniBatch:
      phi = localVB(doc, alpha, newLambda, k, v) 
      
      for (wordID, count) in doc:
        newLambda[wordID] = etaArray[wordID] + count * phi[wordID]
    
    # Converged?
    if :
      break
    
        
  # Delta lambda
  for wordID in newLambda:
    newLambda[wordID] = newLambda[wordID] - etaArray[wordID]
  
  return newLambda
  
def localVB(doc, alpha, lamb, k, v):
  # Global Variables
  VAR_MAX_ITER = 100
  VAR_CONVERGED = 0.001
  
  # Initialization
  gamma = np.random.gamma(100., (1. / 100.), (1, k))
  gamma = gamma[0]
  phi = {}
  
  for round in xrange(VAR_MAX_ITER):
    # E_q[log theta] & E_q[log beta]
    ElogTheta = psi(gamma)
    ElogBeta = elogBeta(lamb, k)
    
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
    
  return phi
    
def phiTimeWordCount(doc, phi, k):
  sum = np.zeros((1, k))
  
  for (wordID, count) in doc:
    sum = sum + phi[wordID] * count
  
  return sum
          
def elogBeta(lamb, k):
    """
    E_q [log(beta) | lambda]
    """
    ElogBeta = {}
  
    # Evaluate the second term of ElogBeta 
    lambdaSumW = np.asarray([0 for i in xrange(k)])
    for wordID in lamb:
      lambdaSumW = lambdaSumW + lamb[wordID]
    
    for wordID in lamb:
      ElogBeta[wordID] = psi(lamb[wordID]) - psi(lambdaSumW)
    
    return ElogBeta  
  
if __name__ == '__main__':
  main()