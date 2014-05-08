import sys,os
import sxcorpus.sxcorpus as sxc
import logging, gensim
from sxsda.sda_framework import get_config
from datetime import datetime



def corpus_dictionary(corpus_fn,dict_fn):
    dictionary = gensim.corpora.Dictionary.load(dict_fn)
    mm = gensim.corpora.MmCorpus(corpus_fn)
    logging.info(repr(dictionary))
    logging.info(repr(mm))
    return mm,dictionary

def online_lda(corpus,dictionary,num_topics,batch_size):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=1, chunksize=batch_size, passes=1)
    return lda


def batch_lda(corpus,dictionary,num_topics):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=0, passes=20)
    return lda

def train():
    '''
    $1 path to config file
    '''
    start = datetime.now()
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    # loading configs;
    t = sys.argv[1]
    config = get_config(sys.argv[2])
    k = config['k']
    nthread = config['nthread']
    asyn = config['asyn']
    mm_path=config['mm_path']
    var_path = config['var_path']
    minibatch = config['minibatch']
    dict_path = config['dict_path']
    corpus,dictionary = corpus_dictionary(mm_path,dict_path)
    V = corpus.num_terms
    output_fn = os.path.join(var_path,'lda')

    if t == 'online':
        lda = online_lda(corpus,dictionary,k,minibatch)
        lda.save(output_fn)
    elif t == 'batch':
        lda = batch_lda(corpus,dictionary,k)
        lda.save(output_fn)

    end = datetime.now()
    print end-start


if __name__ == '__main__':
    train()
