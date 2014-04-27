import sys
import os

def generate_pbs(fn,t,k,name,data_folder):
    content = ['#!/bin/bash','#PBS -l nodes=1:ppn=10','#PBS -l walltime=10:00:00','ROOT=/home/nlg-05/xingshi/workspace/misc/573Final/','cd /home/nlg-05/xingshi/workspace/misc/573Final/py/','DATA=$ROOT/data/%s' % data_folder,'K=%d' % k,'TYPE=%s' % t,'NAME=%s' % name,'CORPUS=$DATA/$NAME.mm','DICT=$DATA/$NAME.dict','ID=$ROOT/model/$NAME.$TYPE.$K','LDA=$ID.lda','LOG=$ID.log.txt','python -m sxlda.sxlda $TYPE $CORPUS $DICT $K $LDA 2>$LOG']
    f = open(fn,'w')
    f.write('\n'.join(content))
    f.close()


def main():
    data_folder = sys.argv[1]
    job_folder = sys.argv[3]
    name = sys.argv[2]
    ts = ['online','batch']
    ks = [10,20,50,100]
    for t in ts:
        for k in ks:
            fn = name+'.'+t+'.'+str(k)+'.pbs'
            path = os.path.join(job_folder,fn)
            generate_pbs(path,t,k,name,data_folder)
            

if __name__ == '__main__':
    main()

