from gensim import corpora
import sys
import logging
import random

def generate_dict(fn,stop_fn,output_fn):
    dictionary = corpora.Dictionary(line.lower().split() for line in open(fn))
    # remove stop words and words only appear once.
    stoplist = [line.strip().lower() for line in open(stop_fn)]
    stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid,docfreq in dictionary.dfs.iteritems() if docfreq == 1]
    dictionary.filter_tokens(stop_ids+once_ids)
    dictionary.compactify()
    dictionary.save(output_fn)

def get_dict(fn):
    dictionary = corpora.Dictionary.load(fn)
    return dictionary

def main_generate_dict():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fn = sys.argv[1]
    stop_fn = sys.argv[2]
    output_fn = sys.argv[3]
    generate_dict(fn,stop_fn,output_fn)

class MyCorpus(object):
    def __init__(self,fn,dictionary):
        self.fn = fn
        self.dictionary = dictionary
    def __iter__(self):
        for line in open(self.fn):
            yield self.dictionary.doc2bow(line.lower().split())
        
def generate_corpus(fn,dict_fn,output_fn):
    dictionary = get_dict(dict_fn)
    corpus = MyCorpus(fn,dictionary)
    corpora.MmCorpus.serialize(output_fn,corpus)

def get_corpus(fn):
    mm = corpora.MmCorpus(fn)
    return mm

def main_generate_corpus():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    fn = sys.argv[1]
    dict_fn = sys.argv[2]
    output_fn = sys.argv[3]
    generate_corpus(fn,dict_fn,output_fn)
    

def generate_split(fn,fn_train,fn_test,ratio):
    f = open(fn)
    f_train= open(fn_train,'w')
    f_test= open(fn_test,'w')
    for line in f:
        ll = line.strip().split()
        train = []
        test = []
        for lll in ll:
            if random.randint(1,100) <= ratio:
                test.append(lll)
            else:
                train.append(lll)
        f_train.write(' '.join(train)+'\n')
        f_test.write(' '.join(test)+'\n')

    f_train.close()
    f_test.close()

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    t = sys.argv[1]
    if t == 'dict':
        fn = sys.argv[2]
        stop_fn = sys.argv[3]
        output_fn = sys.argv[4]
        generate_dict(fn,stop_fn,output_fn)
    elif t == 'corpus':
        fn = sys.argv[2]
        dict_fn = sys.argv[3]
        output_fn = sys.argv[4]
        generate_corpus(fn,dict_fn,output_fn)
    elif t == 'split':
        fn = sys.argv[2]
        ratio_str = sys.argv[3]
        ratio = int(ratio_str)
        fn_train = '.'.join([fn,ratio_str,'train'])
        fn_test = '.'.join([fn,ratio_str,'test'])
        generate_split(fn,fn_train,fn_test,ratio)
        



def demo_corpus():
    fn = sys.argv[1]
    corpus = get_corpus(fn)
    for c in corpus:
        print c



if __name__ == '__main__':
    main()
    #test()
