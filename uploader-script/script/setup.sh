DEST=/Volumes/CIRCUITPY
PY_DIR=../../py/src

cp $PY_DIR/slideshow.py $DEST/ 
cp $PY_DIR/qmi8658.py $DEST/ 
cp $PY_DIR/gc9a01.py $DEST/ 
cp $PY_DIR/code.py $DEST/ 
cp -r $PY_DIR/lib  $DEST/

echo 'setting up images'
mkdir -p $DEST/img/slides
echo 'copy zorb'
cp ./zorb.bmp $DEST/img
echo "copy $1"
cp ./$1*.bmp $DEST/img/slides