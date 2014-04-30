import logging
from multiprocessing import Lock, Pool
import sxsda.eta_alpha as _mea
from sxsda.locked import LockedSum, LockedEta
import sxsda.sda_worker as _mworker
import sys
import os

def callback(delta_eta,lockedEta,nActPro,nBatch,var_path,nthread):
    lockedEta.add_eta(delta_eta)
    nActPro.add_value(-1)
    nBatch.add_value(1)
    nBatch_value = nBatch.get_value()
    if  nBatch_value % nthread == 0:
        fn = 'eta.{}.pickle'.format(nBatch_value/nthread-1)
        path = os.path.join(var_path,fn)
        lockedEta.write_eta(path)
        logging.info('round:{}, batch:{}'.format(nBatch_value/nthread-1,nBatch_value))


def asyn_workder(d,eta,etaSum,alpha):
    delta_eta = _mworker.lda_worker(d,eta,etaSum,alpha)
    return delta_eta


def asyn_framework(corpus,k,V,nthread,minibatch,var_path,record_eta = False):
    # configs
    thread_batch = minibatch/nthread
    # ids 
    doc_id = 0
    batch_id = 0
    round_id = 0
    # temp data
    doc_buffer = []
    voc_temp = set()
    # global data
    lockedEta = LockedEta({},Lock())
    
    # process contral
    pool = Pool(processes = nthread)
    nActPro = LockedSum(0,Lock())
    nBatch = LockedSum(0,Lock())
    results = []
    for doc in corpus:
        
        for vid,count in doc:
            voc_temp.add(vid)
        doc_buffer.append(doc)

        if doc_id % thread_batch == thread_batch - 1:
            eta_temp = lockedEta.get_eta(k,voc_temp)
            etaSum = lockedEta.get_eta_sum(k,V)
            alpha = _mea.get_alpha(k)
            while True: # check for active processes amount
                if nActPro.get_value() < nthread:
                    break
                
            cb = lambda x: callback(x,lockedEta,nActPro,nBatch,var_path,nthread)
            result = pool.apply_async(asyn_workder,(doc_buffer,eta_temp,etaSum,alpha),callback = cb)
            results.append(result)
            nActPro.add_value(1)
            
            # clear buffer
            doc_buffer = []
            voc_temp = set()
            batch_id += 1

            
        doc_id += 1

    # some remain doc may not be processed
    if len(doc_buffer) > 0:
        eta_temp = lockedEta.get_eta(k,voc_temp)
        etaSum = lockedEta.get_eta_sum(k,V)
        alpha = _mea.get_alpha(k)
        while True: # check for active processes amount
            if nActPro.get_value() < nthread:
                break
                
        cb = lambda x: callback(x,lockedEta,nActPro,nBatch,var_path,nthread)
        result = pool.apply_async(asyn_workder,(doc_buffer,eta_temp,etaSum,alpha),callback = cb)
        results.append(result)
        nActPro.add_value(1)
        batch_id += 1

    for r in results:
        r.wait()

    if nBatch.get_value() % nthread != 0:
        nBatch_value = nBatch.get_value()
        fn = 'eta.{}.pickle'.format(nBatch_value/nthread)
        path = os.path.join(var_path,fn)
        lockedEta.write_eta(path)
        
    return lockedEta.eta
