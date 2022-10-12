DEST=/Volumes/CIRCUITPY

cp ../../slideshow.py $DEST/ 
cp ../../qmi8658.py $DEST/ 
cp ../../gc9a01.py $DEST/ 
cp ../../code.py $DEST/ 
cp -r ../../lib  $DEST/

echo 'setting up images'
mkdir -p $DEST/img/slides
echo 'copy zorb'
cp ./zorb.bmp $DEST/img
echo 'copy poaps'
cp ./poap*.bmp $DEST/img/slides