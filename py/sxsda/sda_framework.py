import sxsda.sda_worker as _mWorker
import sxcorpus.sxcorpus as _mCorpus
from sxcorpus.sxcorpus import MyCorpus
import sxsda.eta_alpha as _mea
import sxsda.syn_framework as _msynf
import sxsda.asyn_framework as _masynf
import sxsda.syn_f
import cPickle
import logging


#### utils ####

def get_config(fn):
    config = {}
    f = open(fn)
    for line in f:
        fields = line.strip().split('=')
        assert(len(fields)==2)
        t = fields[0]
        key = fields[1]
        value = fields[2]
        if t == 'i': #int
            config[key] = int(value)
        elif t== 'f': #float
            config[key] = float(value)
        elif t=='s': # string
            config[key] = value
        elif t=='b': # bool
            config[key]= bool(value)
    return config


def main():
    '''
    $1 path to config file
    '''
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading configs;
    config = get_config(sys.argv[1])
    k = config['k']
    nthread = config['nthread']
    asyn = config['asyn']
    mm_path=config['mm_path']
    var_path = config['var_paht']
    minibatch = config['minibatch']
    
    corpus = _mCorpus.get_corpus(mm_path)

    if asyn:
        _masynf.asyn_master(corpus,k,nthread,minibatch,var_path)
    else:
        _msynf.syn_master(corpus,k,nthread,minibatch,var_path)


if __init__ == '__main__':
    main()
