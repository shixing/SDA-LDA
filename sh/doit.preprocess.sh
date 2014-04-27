# $1 data files
source ./setenv.sh
_NAME=$DATA/1000
_DATA=$_NAME.txt
_DICT=$_NAME.dict
_MM=$_NAME.mm

cd $PY

python -m sxcorpus.sxcorpus dict $_DATA $STOPWORDS $_DICT
python -m sxcorpus.sxcorpus corpus $_DATA $_DICT $_MM
