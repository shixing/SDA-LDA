# $1 data files
# $2 ratio: integer between 1 and 100
source ./setenv.sh
_DATA=$DATA/$1

cd $PY

#python -m sxcorpus.sxcorpus dict $_DATA $STOPWORDS $_DICT
python -m sxcorpus.sxcorpus split $_DATA $2
