# usage:
# bash doit.clean.sh 
# clean all files with ~
source setenv.sh
echo $ROOT
FILES=`find $ROOT/. | grep '~' `
FILES1=`find $ROOT/. | grep '#' `
echo $FILES
echo $FILES1
echo 'Delete all these files? y/[n]'
read input_variable
if [ $input_variable == 'y' ];then
    rm $FILES
    rm $FILES1
fi
