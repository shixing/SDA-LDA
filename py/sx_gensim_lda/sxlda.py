import sys
import sxcorpus.sxcorpus as sxc
import logging, gensim

def corpus_dictionary(corpus_fn,dict_fn):
    dictionary = gensim.corpora.Dictionary.load(dict_fn)
    mm = gensim.corpora.MmCorpus(corpus_fn)
    logging.info(repr(dictionary))
    logging.info(repr(mm))
    return mm,dictionary

def online_lda(corpus,dictionary,num_topics):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=1, chunksize=500, passes=1)
    return lda


def batch_lda(corpus,dictionary,num_topics):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, update_every=0, passes=20)
    return lda

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    t = sys.argv[1]
    corpus_fn = sys.argv[2]
    dict_fn = sys.argv[3]
    num_topics = int(sys.argv[4])
    output_fn = sys.argv[5]
    if t == 'online':
        corpus,dictionary = corpus_dictionary(corpus_fn,dict_fn)
        lda = online_lda(corpus,dictionary,num_topics)
        lda.save(output_fn)
    elif t == 'batch':
        corpus,dictionary = corpus_dictionary(corpus_fn,dict_fn)
        lda = batch_lda(corpus,dictionary,num_topics)
        lda.save(output_fn)


if __name__ == '__main__':
    main()
