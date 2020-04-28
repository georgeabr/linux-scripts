#!/bin/sh

# shows the compression ratio for each file in the specified folder
# it adds a leading zero, if value less than 1
# for example: ./zfs-ratio.sh /opt/ /bin/ /var/ /usr/ /etc/ /boot/ 2>/dev/null
# Ratio     Size     Name
# =========================
# 01.42 -    6105M - /usr/
# 01.26 -    1536M - /var/
# 01.86 -    2495M - /lib/
# 01.70 -     186M - /bin/
# 00.46 -      10M - /etc/
# 01.19 -    6656M - /home/
# 01.51 -     121M - /opt/

printf "Ratio     Size     Name\n"
printf "=========================\n"
for i in $* ; do
  actualsize=`du -s --apparent-size $i 2>/dev/null|awk '{print $1}'`
  compressedsize=`du -s $i 2>/dev/null|awk '{print $1}'`
  var3=$(echo "scale=2;if (($actualsize/$compressedsize) < 1) print 0; if (($actualsize/$compressedsize) < 10) print 0; print ($actualsize/$compressedsize)" | bc)
  # printf "$var3 - "; du -d0 -BM $i 2>/dev/null| awk '{print $1 " - " $2}'
  # awk '{ s = "00000000"$1; print substr(s, 1 + length(s) - 8); }' # 8 leading spaces for "size" column
  printf "$var3 - "; du -d0 -BM $i 2>/dev/null| awk '{s = "        "$1; print substr(s, 1 + length(s) - 8) " - " $2}'
done
