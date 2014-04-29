import sxsda.sda_worker as _mWorker
import sxcorpus.sxcorpus as _mCorpus
from sxcorpus.sxcorpus import MyCorpus
import sxsda.eta_alpha as _mea
import sxsda.syn_framework as _msynf
import sxsda.asyn_framework as _masynf
import sxsda.perplexity as _mper
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


def train():
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
    var_path = config['var_path']
    minibatch = config['minibatch']
    corpus = _mCorpus.get_corpus(mm_path)
    V = corpus.num_terms
    if asyn:
        eta = _masynf.asyn_master(corpus,k,V,nthread,minibatch,var_path)
    else:
        eta = _msynf.syn_master(corpus,k,V,nthread,minibatch,var_path)

    fn = 'eta.final.pickle'
    path = os.path.join(var_path,fn)
    _mea.write_eta(eta,path)

def test():
    '''
    $1 path to config file
    '''
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading configs;
    config = get_config(sys.argv[1])
    k = config['k']
    test_path = config['test_path']
    test_train_path = config['test_train']
    test_test_path = config['test_test']
    eta_path = config['eta_path']
    
    corpus = _mCorpus.get_corpus(test_path)
    V = corpus.num_terms

    voc_set = set()
    for doc in corpus:
        for wid,count in doc:
            woc_set.add(wid)

    eta = _mea.load_eta(eta_path)
    etaTest = _mea.get_eta(k,eta,voc_set)
    etaSum = _mea.get_eta_sum(eta,k,V)
    test_test = _mea.load_eta(test_test_path)
    test_train = _mea.load_eta(test_train_path)
    alpha = _mea.get_alpha(k)
    perplexity = _mper.perplexity(test_train,test_test,alpha,etaTest,etaSum)
    
    print perplexity

if __init__ == '__main__':
    main()
