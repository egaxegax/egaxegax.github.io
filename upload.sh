#!/bin/sh

mdir=`dirname $0`

lftp <<EOF
set ssl:verify-certificate no
open ftp://u2774856:Hae1mz2qo59lnAQF@egax.ru
ls /www/egax.ru
mirror --reverse --delete -x .git $mdir /www/egax.ru
mirror --reverse --delete -x .git $mdir/../dbcartajs /www/egax.ru/dbcartajs
exit
EOF
