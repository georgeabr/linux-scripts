#!/bin/sh

for i in $* ; do
actualsize=`du -s --apparent-size $i |awk '{print $1}'`
compressedsize=`du -s $i |awk '{print $1}'`
var3=$(echo "scale=2;if (($actualsize/$compressedsize) < 1) print 0; print ($actualsize/$compressedsize)" | bc)
printf "$var3 - $i\n"
done