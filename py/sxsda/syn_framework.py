import logging
import os
import sys
import sxsda.eta_alpha as _mea
from multiprocessing import Process,Queue
import sxsda.sda_worker as _mworker

def syn_framework(corpus,k,V,nthread,minibatch,var_path,record_eta = False):
    # configs
    thread_batch = minibatch/nthread
    # ids 
    doc_id = 0
    batch_id = 0
    round_id = 0
    # temp data
    doc_buffer = []
    batch_buffer = [] # [(docs,etas)]
    voc_temp = set()
    # global data
    eta = {}

    for doc in corpus:

        for vid,count in doc:
            voc_temp.add(vid)
        doc_buffer.append(doc)

        if doc_id % thread_batch == thread_batch - 1:
            eta_temp = _mea.get_eta(k,input_eta = eta, voc_set = voc_temp)
            etaSum = _mea.get_eta_sum(eta,k,V)
            batch_buffer.append((doc_buffer,eta_temp,etaSum))
            
            # clear doc buffer
            doc_buffer = []
            voc_temp = set()
            
            if batch_id % nthread == nthread - 1:
                # update eta
                eta = syn_master(batch_buffer,k,nthread,eta,_mea.get_alpha(k))
                if record_eta:
                    fn = 'eta.{}.pickle'.format(round_id)
                    path = os.path.join(var_path,fn)
                    _mea.write_eta(eta,path)
                # clear batch_buffer
                batch_buffer = []
                round_id += 1
                logging.info('round:{}, batch:{}'.format(round_id,batch_id))

            batch_id += 1
            


        doc_id += 1


    # process the docs in current doc_buffer
    if len(doc_buffer) > 0:
        # form a new batch
        eta_temp = _mea.get_eta(k,input_eta = eta, voc_set = voc_temp)
        etaSum = _mea.get_eta_sum(eta,k,V)
        batch_buffer.append((doc_buffer,eta_temp,etaSum))
        
        # form a new round
        eta = syn_master(batch_buffer,k,len(batch_buffer),eta,_mea.get_alpha(k))
        if record_eta:
            fn = 'eta.{}.pickle'.format(round_id)
            path = os.path.join(var_path,fn)
            _mea.write_eta(eta,path)

        round_id +=1
        batch_id +=1

    return eta

def syn_master(batch_buffer,k,n_core,eta,alpha):
    new_eta = eta

    processes = []
    q = Queue()

    for i in xrange(n_core):
        d,eta,etaSum = batch_buffer[i]
        prc = Process(target = syn_worker, args = (d,eta,etaSum,alpha,q))
        processes.append(prc)
        prc.start()
        
    for i in xrange(n_core):
        delta_eta = q.get()
        _mea.add_eta(new_eta,delta_eta)
        
    for prc in processes:
        prc.join()
        
    return new_eta

def syn_worker(d,eta,etaSum,alpha,q):
    delta_eta =  _mworker.lda_worker(d,eta,etaSum,alpha)
    q.put(delta_eta)
