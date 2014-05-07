# Asynchronized Multi-machine version using MPICH
# parallel in two level, not three level.
# How to run:
# mpiexec -np 10 python -m sxsda.sda_framework_mpi train ../config/train.1.config
#

import sxcorpus.sxcorpus as _mCorpus
from sxcorpus.sxcorpus import MyCorpus
from mpi4py import MPI
from datetime import datetime
from sxsda.sxutils import enum
from sxsda.sda_framework import get_config
from sxsda.mpi_master_worker import master_process, worker_process
import sxsda.eta_alpha as _mea
import sys
import os
import cPickle
import logging

def main():
    # Initializations and preliminaries
    comm = MPI.COMM_WORLD   # get MPI communicator object
    size = comm.size        # total number of processes
    rank = comm.rank        # rank of this process
    status = MPI.Status()   # get MPI status object
    tags = enum('READY', 'DONE', 'EXIT', 'START')

    if rank == 0:
        # Master process
        '''
        $1 path to config file
        '''
        start = datetime.now()
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

        # loading configs;
        config = get_config(sys.argv[2])
        k = config['k']
        nthread = config['nthread']
        asyn = config['asyn'] # here, the value should be 'mpi'
        mm_path=config['mm_path']
        var_path = config['var_path']
        minibatch = config['minibatch']
        corpus = _mCorpus.get_corpus(mm_path)
        V = corpus.num_terms
        
        eta = master_process(comm,status,tags,corpus,k,V,nthread,minibatch,var_path)
        
        # store the final pickle
        fn = 'eta.final.pickle'
        path = os.path.join(var_path,fn)
        _mea.write_eta(eta,path)

        end = datetime.now()
        print end-start

    else:
        # Worker process
        name = MPI.Get_processor_name()
        worker_process(comm,status,tags,name)


#def mpi_framework(corpus,k,V,nthread,minibatch,var_path,record_eta = False):
    


if __name__ == '__main__':
    main()
