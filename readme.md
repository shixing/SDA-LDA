### Introduction

This project is a Python implementation of Streaming(S) Distributed(D) Asynchronous LDA (SDA-LDA), based on the idea of the paper [Streaming Variational Bayes](http://www.cs.berkeley.edu/~wibisono/sda-bayes.pdf). Feel free to use this package.

Note: cd in folder `py` to run the following command.

### Data preprocessing

First, you data file `data` should be one document per line.

#### Generate Dictionary File
```
python -m sxcorpus.sxcorpus dict data stop_file_path data.dict
```

#### Generate Training File
```
python -m sxcorpus.sxcorpus corpus train data.dict train.mm
```
This command will convert the one doc per line file `train` into a mm-format file `train.mm`

#### Generate Test File
Sample from your test data, sample rate = 10%
```
python -m sxcorpus.sxcorpus split test 10
```
The command will generate two files `test.test.10` and `test.train.10`, then you need to convert these two file into mm-format.

### Train

#### LDA using gensim
##### online training
```
python -m sx_gensim_lda.sxlda online ../config/train.1.config
```

##### batch training
```
python -m sx_gensim_lda.sxlda batch ../config/train.1.config
```

#### Multi-core SDA-LDA
#####Synchronous Training
First, in config file (train.1.config), set asyn=False, then run:
```
python -m sxsda.sda_framework train ../config/train.1.config
```
#####Asynchronous Training
Set asyn=True in config file, then run the same command above

#### Multi-machine SDA-LDA (MPI based)

Run on a single machine with MPI
```
mpiexec -np 3 python -m sxsda.sda_framework_mpi train ../config/train.1.config
```

Run on a PBS cluster with MPI
```
cd jobs
qsub sda_64t_14.jobs # start 64 processes with mini-batch size = 2^14 documents
```

### Test
Calculate the log predictive probability on test set.
```
python -m sxsda.sda_framework test ../config/test.1.config
```

### Contact

Xing Shi xingshi@usc.edu
Hsuan-yi Chu hsuanyi@usc.edu