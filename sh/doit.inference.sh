# $1 config files
source ./setenv.sh

_CONFIG=$CONFIG/$1

cd $PY

python -m sxsda.sda_framework train $_CONFIG
