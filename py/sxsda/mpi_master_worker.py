from mpi4py import MPI
import logging
from multiprocessing import Lock, Pool
import sxsda.eta_alpha as _mea
from sxsda.locked import LockedSum, LockedEta
import sxsda.sda_worker as _mworker
import sys
import os


def batch_generator(corpus,k,V,thread_batch,lockedEta):
    # ids 
    doc_id = 0
    batch_id = 0
    round_id = 0
    # temp data
    doc_buffer = []
    voc_temp = set()
    
    # process contral
    nBatch = LockedSum(0,Lock())

    for doc in corpus:
        
        for vid,count in doc:
            voc_temp.add(vid)
        doc_buffer.append(doc)

        if doc_id % thread_batch == thread_batch - 1:
            eta_temp = lockedEta.get_eta(k,voc_temp)
            etaSum = lockedEta.get_eta_sum(k,V)
            alpha = _mea.get_alpha(k)
            
            yield (doc_buffer,eta_temp,etaSum,alpha,batch_id)

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

        yield (doc_buffer,eta_temp,etaSum,alpha,batch_id)

        batch_id += 1    


def master_process(comm,status,tags,corpus,k,V,nthread,minibatch,var_path,record_eta = False):

    # parameter for threads
    num_workers = comm.size - 1
    task_id = 0
    closed_workers = 0
    logging.info('Master start with {} works'.format(num_workers))

    thread_batch = minibatch/nthread
    lockedEta = LockedEta({},Lock())
    bg = batch_generator(corpus,k,V,thread_batch,lockedEta)
    last_doc_seen = 0


    while closed_workers < num_workers:
        data = comm.recv(source = MPI.ANY_SOURCE, tag = MPI.ANY_TAG, status = status)
        source = status.Get_source()
        tag = status.Get_tag()
        
        if tag == tags.READY:
            try:
                if source <= nthread:
                    doc_buffer,eta_temp,etaSum,alpha,batch_id = next(bg)
                    comm.send((doc_buffer,eta_temp,etaSum,alpha,batch_id),dest = source,tag = tags.START)
                else:
                    comm.send(None, dest = source, tag = tags.EXIT)
            except StopIteration:
                comm.send(None, dest = source, tag = tags.EXIT)
        elif tag == tags.DONE:
            delta_eta, nBatch_value = data
            nBatch_value += 1
            logging.info('Got batch {} results from worker {}'.format(nBatch_value,source))
            lockedEta.add_eta(delta_eta)
            doc_seen = nBatch_value * minibatch * 1.0
            if doc_seen - last_doc_seen >= 200000:
                fn = 'eta.{}.pickle'.format(nBatch_value/nthread-1)
                path = os.path.join(var_path,fn)
                lockedEta.write_eta(path)
                logging.info('round:{}, batch:{}'.format(nBatch_value/nthread-1,nBatch_value))
                last_doc_seen = doc_seen

        elif tag == tags.EXIT:
            logging.info('Worker {} exited.'.format(source))
            closed_workers += 1

    return lockedEta.eta

    

def worker_process(comm,status,tags,name):
    rank = comm.rank
    logging.info("I am a worker with rank %d on %s." % (rank, name))
    while True:
        comm.send(None, dest=0, tag=tags.READY)
        data = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
        tag = status.Get_tag()
        
        if tag == tags.START:
            # Do the work here
            d,eta,etaSum,alpha,bid = data
            delta_eta = _mworker.lda_worker(d,eta,etaSum,alpha)
            comm.send((delta_eta,bid), dest=0, tag=tags.DONE)
        elif tag == tags.EXIT:
            break

    comm.send(None, dest=0, tag=tags.EXIT)

        
