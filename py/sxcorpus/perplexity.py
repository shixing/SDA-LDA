import numpy as np
import math

def testVal(testDocs, gamma, lamb):
  numerator = 0.
  denominator = 0.
  
  for doc in testDocs:  
    for (wordID, counts) in doc:
      numerator = numerator + logPW(wordID, gamma, lamb)
      denominator = denominator + counts
      
  return numerator / denominator
  
def logPW(wordID, gamma, lamb):
  k = len(gamma)
  lambOfWord = lamb[wordID]
  
  term = 0
  for i in xrange(k):
    term = term + (gamma[i] / sum(gamma)) * (lambOfWord[i] / sum(lambOfWord))
    
  return log(term)
  
if __name__ == '__main__':
  main()