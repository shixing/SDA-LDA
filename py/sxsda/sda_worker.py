import numpy as np
from scipy.special import psi
from scipy.special import gamma as gammaFu
from scipy.special import polygamma
from scipy.misc import logsumexp
from sxsda.sxmath import mylogsumexp
import random
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


def lda_worker(miniBatch, eta, etaSum, alpha, debug = True):
  # Global Variables
  VAR_MAX_ITER = 10
  VAR_CONVERGED = 0.01
 
  # Initialization
  k = len(alpha)
  alpha = np.asarray(alpha)
  eta_2d, widMap = eta_dict_to_array(eta,k) # widMap wid->colum_id in eta_2d; eta_2d is k*len(widMap)
  oldLambda_2d = None
  newLambda_2d = np.array(eta_2d)
  etaSum = np.asarray(etaSum)
  nConvergedDoc = 0

  for round in xrange(VAR_MAX_ITER): 
    if debug:
      print round
    nConvergedDoc = 0
    
    oldLambda_2d = np.array(newLambda_2d)
    expElogBeta = expElogBetaF(newLambda_2d, etaSum,widMap) # dict 
    newLambda_2d = np.array(eta_2d)

    # Process each document
    for doc in miniBatch:  
      # phi_cts is k*len(doc) array, = phi_dvk*n_dv
      phi_cts,ids, _, ncd = localVB(doc, alpha, k, expElogBeta)
      nConvergedDoc += ncd
      
      # update newLambda
      for i,wid in enumerate(ids):
        column_id = widMap[wid]
        newLambda_2d[:,column_id] += phi_cts[:,i]

    if debug:
      print '# converge doc:{}/{}'.format(nConvergedDoc,len(miniBatch))

      
    # Update etaSum
    etaSum += newLambda_2d.sum(axis = 1) - oldLambda_2d.sum(axis = 1)
    
    # Converged?
    meanchange = np.mean(np.abs(oldLambda_2d-newLambda_2d))
    if (meanchange < VAR_CONVERGED):
      break
        
  # Delta lambda
  valReturn = {}
  delta_Lambda_2d = newLambda_2d - eta_2d
  for wid in widMap:
    column_id = widMap[wid]
    valReturn[wid] = list(delta_Lambda_2d[:,column_id])
  

  return valReturn


# based on Lee&Seung trick, don't calculate phi, calculate update gamma directly
def localVB(doc, alpha, k, expElogBeta):
  # Global Variables
  VAR_MAX_ITER = 10
  VAR_CONVERGED = 0.01
  isConverged = 0
  # Initialization
  ids = [id for id,_ in doc]
  cts = np.array([cnt for _,cnt in doc])
  
  gamma = np.asarray([1.0 / k  for i in xrange(k)]) # 1*k
  expElogTheta = np.exp(psi(gamma)) # 1*k
  
  expElogBetaD = expElogBeta_k_by_d(expElogBeta,k,ids)  # k*d
  phinorm = np.dot(expElogTheta,expElogBetaD) + 1e-100 # 1 * d
  
  for round in xrange(VAR_MAX_ITER):

    lastgamma = gamma
    gamma = alpha + expElogTheta * np.dot(cts/phinorm, expElogBetaD.T)
    
    expElogTheta = np.exp(psi(gamma))
    phinorm = np.dot(expElogTheta,expElogBetaD) + 1e-100 # 1 * d
    # isConverged ?
    meanchange = np.mean(abs(gamma - lastgamma))
    if (meanchange < VAR_CONVERGED):
      isConverged = 1
      break

  # calculate phi
  
  phi_cts = np.dot( np.dot( np.diag(expElogTheta), expElogBetaD), np.diag(cts/phinorm))

  return phi_cts,ids,gamma,isConverged

    
def phiTimeWordCount(doc, phi, k):
  sum = np.asarray([0 for i in xrange(k)])
  
  for (wordID, count) in doc:
    sum = sum + phi[wordID] * count
  
  return sum


def expElogBetaF(lamb, etaSum, widMap=None):
    """
    E_q [log(beta) | lambda]
    """
    if type(lamb) == dict: # lamb is dict
      expElogBeta = {}
    # Evaluate the second term of ElogBeta
      psiEtaSum = psi(etaSum)
      for wordID in lamb:
        expElogBeta[wordID] = np.exp(psi(lamb[wordID]) - psiEtaSum)
      return expElogBeta  
    else: # lamb is k*d array
      expElogBeta = {}
    # Evaluate the second term of ElogBeta
      psiEtaSum = psi(etaSum)
      for wid in widMap:
        column_id = widMap[wid]
        expElogBeta[wid] = np.exp(psi(lamb[:,column_id]) - psiEtaSum)
      return expElogBeta  
   

def expElogBeta_k_by_d(expElogBeta,k,ids):
  expElogBetaD = np.zeros((k,len(ids)))
  for i in xrange(len(ids)):
    wid = ids[i]
    expElogBetaD[:,i] = expElogBeta[wid]

  return expElogBetaD


def eta_dict_to_array(eta,k):
  eta_array = np.zeros((k,len(eta)))
  widMap = {}
  i = 0
  for wid in eta:
    widMap[wid] = i
    eta_array[:,i] = eta[wid]
    i+=1
  return eta_array,widMap


  
  
if __name__ == '__main__':
  main()
