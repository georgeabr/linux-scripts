#!/bin/sh

# shows the compression ratio for each file in the specified folder
# it adds a leading zero, if value less than 1
# for example ./zfs-ratio.sh /bin/*
# 1.00 - /bin/ypdomainname
# 1.20 - /bin/zgrep
# 0.40 - /bin/zless
# 0.40 - /bin/zmore
# 1.00 - /bin/znew

for i in $* ; do
actualsize=`du -s --apparent-size $i |awk '{print $1}'`
compressedsize=`du -s $i |awk '{print $1}'`
var3=$(echo "scale=2;if (($actualsize/$compressedsize) < 1) print 0; if (($actualsize/$compressedsize) < 10) print 0; print ($actualsize/$compressedsize)" | bc)
printf "$var3 - $i\n"
done
