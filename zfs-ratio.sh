#!/bin/sh

# shows the compression ratio for each file in the specified folder
# it adds a leading zero, if value less than 1
# for example: ./zfs-ratio.sh /opt/ /bin/ /var/ /usr/ /etc/ /boot/ 2>/dev/null
# 01.51 - /opt/
# 01.71 - /bin/
# 01.08 - /var/
# 01.40 - /usr/
# 00.46 - /etc/
# 01.03 - /boot/
# or
# 01.51  - 121M   /opt/
# 01.71  - 182M   /bin/
# 01.08  - 2.9G   /var/
# 01.40  - 5.7G   /usr/
# 00.46  - 9.0M   /etc/
# 01.03  - 199M   /boot/


for i in $* ; do
  actualsize=`du -s --apparent-size $i 2>/dev/null|awk '{print $1}'`
  compressedsize=`du -s $i 2>/dev/null|awk '{print $1}'`
  var3=$(echo "scale=2;if (($actualsize/$compressedsize) < 1) print 0; if (($actualsize/$compressedsize) < 10) print 0; print ($actualsize/$compressedsize)" | bc)
  # printf "$var3 - $i\n"
  printf "$var3 - "; du -d0 -h $i 2>/dev/null

done
