#!/bin/sh

lftp <<EOF
set ssl:verify-certificate no
open ftp://u2774856:Hae1mz2qo59lnAQF@egax.ru
ls /www/egax.ru
mirror --reverse --delete -x .git -x __pycache__ /home/agena/NetBeansProjects/egaxegax.github.io /www/egax.ru
mirror --reverse --delete -x .git /home/agena/NetBeansProjects/dbcartajs /www/egax.ru/dbcartajs
exit
EOF
