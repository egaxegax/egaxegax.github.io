#!/bin/sh

dom="egax.ru"
userpass="u2774856:Hae1mz2qo59lnAQF"
tgtdir=`dirname $0`

if [ $1 == "" ]; then exit 1; fi

lftp <<EOF
set ssl:verify-certificate no
open ftp://$userpass@$dom
put $tgtdir/$1 -o /www/$dom/$1
exit
EOF