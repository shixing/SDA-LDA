# generate config for hpc
source ./setenv.sh

function generate()
{
k=$1
mini=$2
thread=$3
thread1=$(( $thread + 1 ))
asyn=$4
fn=$CONFIG/train.$k.$mini.$thread.$asyn.config;
_TRAIN=train.$k.$mini.$thread.$asyn.config;
vf=$VAR/$k.$mini.$thread.$asyn;
mkdir $vf
echo $fn
echo "i=k=$k" > $fn
echo "i=nthread=$thread" >> $fn
echo "s=mm_path=$DATA/4000.mm" >> $fn
echo "b=asyn=$asyn" >> $fn
echo "s=var_path=$vf/" >> $fn
echo "i=minibatch=$mini" >> $fn

fn=$CONFIG/test.$k.$mini.$thread.$asyn.config;
_TEST=test.$k.$mini.$thread.$asyn.config;
echo $fn
echo "i=k=$k" > $fn
echo "s=test_path=$DATA/400.mm" >> $fn
echo "s=test_train=$DATA/400.10.train.mm" >> $fn
echo "s=test_test=$DATA/400.10.test.mm" >> $fn
echo "s=eta_path=$vf/eta.final.pickle" >> $fn

# generate jobs;
fn=$JOBS/$k.$mini.$thread.$asyn.pbs;
_LOG=$LOG/$k.$mini.$thread.$asyn.log.txt;
_PER=$LOG/$k.$mini.$thread.$asyn.per.txt;
echo $fn
echo "#!/bin/bash" > $fn
echo "#PBS -l nodes=1:ppn=$thread" >> $fn
echo "#PBS -l walltime=10:00:00" >> $fn
echo "cd /home/nlg-05/xingshi/workspace/misc/573Final/sh/" >> $fn
echo "bash doit.inference.sh $_TRAIN > $_LOG" >> $fn
echo "bash doit.test.sh $_TEST > $_PER" >> $fn
	    
}

# compare topic
for k in 10 50 100; do
    generate $k 432 12 False
done;

# compare MINI
for mini in 72 432; do 
    generate 10 $mini 12 False
done;

# compare thread
for thread in 4 8 12; do
    generate 10 432 $thread False
done;

# compare asyn
for asyn in True False; do
    generate 10 432 8 $asyn
done




