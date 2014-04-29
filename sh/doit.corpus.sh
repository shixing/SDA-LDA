# $1 data file name
source ./setenv.sh
_NAME=$DATA/$1
_DATA=$_NAME
_DICT=$DATA/short_abstracts_en.dict
_MM=$_NAME.mm

cd $PY

#python -m sxcorpus.sxcorpus dict $_DATA $STOPWORDS $_DICT
python -m sxcorpus.sxcorpus corpus $_DATA $_DICT $_MM
