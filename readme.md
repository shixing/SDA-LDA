Note: cd in folder `py` to run the following command.
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

#### Multi-machine (MPI based)
```
mpiexec -np 3 python -m sxsda.sda_framework_mpi train ../config/train.1.config
```

#### Test
```
python -m sxsda.sda_framework test ../config/test.1.config
```
