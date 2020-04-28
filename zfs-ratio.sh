#!/bin/sh

# shows the compression ratio for each file in the specified folder
# it adds a leading zero, if value less than 1
# for example: ./zfs-ratio.sh /opt/ /bin/ /var/ /usr/ /etc/ /boot/ 2>/dev/null
# Ratio - size - name
# ===================
# 01.42 - 6.0G - /usr/
# 01.26 - 1.5G - /var/
# 01.86 - 2.5G - /lib/

printf "Ratio - size - name\n"
printf "===================\n"
for i in $* ; do
  actualsize=`du -s --apparent-size $i 2>/dev/null|awk '{print $1}'`
  compressedsize=`du -s $i 2>/dev/null|awk '{print $1}'`
  var3=$(echo "scale=2;if (($actualsize/$compressedsize) < 1) print 0; if (($actualsize/$compressedsize) < 10) print 0; print ($actualsize/$compressedsize)" | bc)
  printf "$var3 - "; du -d0 -h $i 2>/dev/null| awk '{print $1 " - " $2}'
done
