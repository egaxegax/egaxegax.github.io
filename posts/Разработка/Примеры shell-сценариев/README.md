<!----><!--2012-11-20 20:10:44-->
## Python Расширенный аналог утилиты wc в Linux
Скрипт рекурсивно считает число строк в файлах каталогов. 
Можно задавать маски поиска имен файлов на вхождение или не вхождение. 
Скрипт использовался в средах Windows и Linux (локаль koi8-r) для версии языка Python 2.4. 
Подробности вызова смотри в исходнике или в справке при вызове без параметров:

    python pywc.py

Текст:
```python
# -*- coding: utf-8 -*-

"""Выводит число строк, байт для каждого файла каталога рекурсивно и итоговую строку."""

import sys, os, re
import fileinput as i
import fnmatch as f

__version__ = '0.3'

E = lambda text: text.encode( {'posix':'koi8-r', 'nt':'cp866'}.get( os.name ) )
_E = lambda text: text.decode( {'posix':'koi8-r', 'nt':'cp866'}.get( os.name ) )
E_OS = lambda text: text.encode( {'posix':'koi8-r', 'nt':'cp1251'}.get( os.name ) )
_E_OS = lambda text: text.decode( {'posix':'koi8-r', 'nt':'cp1251'}.get( os.name ) )

STR_HELP = u"""\
Вызов: python pywc.py <папка> [<файл_масок> | - ]
Выводит число строк, байт для каждого файла в ПАПКЕ по маскам из ФАЙЛА_МАСОК.

ФАЙЛ_МАСОК содержит маски поиска на включение и исключение файлов, разделенных пустой строкой.
Если ФАЙЛ_МАСОК задан как -, читает стандартный ввод, если не задан, подсчитываются все файлы.

Пример файла:
  # включать
  *.c *.cpp
  *.h *.asm

  # исключать
  *\.svn\* *\stdafx.h

Примеры использования:
  python pywc.py .               Считать все файлы в текущем каталоге и ниже. 
  python pywc.py тест1 dir       Считать файлы в test1 и ниже, используя файл масок dir."""

REG_COL = '( ?:[ \t]*#.*\r?\n? )*( ( ?:[^\r\n]+\r?\n? )+ )'
REG_ROW = '( [^ \t\r\n]+ )'

def subinfo( lines, size, files, _files, ts, lastprint=True ):
    """Выводит расчеты в stdout."""
    print lines, size, ts
    print E( u'Посчитано файлов' ), files, E( u'из' ), files + _files             
    if ( lastprint ):
        print

args = sys.argv[1:]

if ( not args ):
    print E( STR_HELP )
    sys.exit( 2 )

# файл масок поиска и исключений
_wcfile = []
if ( len( args ) > 1 ):
    if ( args[1] == '-' ):
        wcfile = sys.stdin
    else:
        wcfile = file( args[1] )
    _wcfile = re.findall( REG_COL, _E_OS( wcfile.read(  ) ) )

res = []
for x in _wcfile:
    res += [re.findall( REG_ROW, x )]

# каталог подсчетов    
os.chdir( args[0] )

dd = sublines = subsize = subfiles = _subfiles = None
totallines = totalsize = totalfiles = _totalfiles = 0
for root, dirs, files in os.walk( u'.', topdown=False ):
    # подпапки
    if ( root != dd ):
        if ( sublines ):
            subinfo( sublines, subsize, subfiles, _subfiles, E( u'ИТОГО' ) )
        sublines = subsize = subfiles = _subfiles = 0
        dd = root
    for name in files:
        curname = os.path.normpath( os.path.join( root, name ) )
        absname = os.path.join( _E_OS( os.getcwd(  ) ), curname )
        if ( res ):      
            p = e = False        
            # вхождения
            for x in res[0]:
                p = ( f.fnmatch( name, x ) or f.fnmatch( curname, x ) or f.fnmatch( absname, x ) )
                if ( p ):
                    break
            # исключения
            if ( len( res ) > 1 and p ):            
                for x in res[1]:
                    e = ( f.fnmatch( name, x ) or f.fnmatch( curname, x ) or f.fnmatch( absname, x ) )
                    if ( e ):
                        break                    
            if ( not ( p and ( not e ) ) ):
                print >> sys.stderr, E( u'Игнорируем' ), E( curname )
                _subfiles += 1
                _totalfiles += 1
                continue
        for line in i.input( E_OS( absname ) ):
            pass
        else:
            curlines, cursize = i.filelineno(  ), os.stat( curname )[6]            
            # по подпапкам
            sublines += curlines
            subsize += cursize
            subfiles += 1
            # всего
            totallines += curlines
            totalsize += cursize
            totalfiles += 1
            print curlines, cursize, E( curname )
            i.close()
else:
    if ( sublines ):
        subinfo( sublines, subsize, subfiles, _subfiles, E( u'ИТОГО' ) )

if ( totallines ):
    subinfo( totallines, totalsize, totalfiles, _totalfiles, E( u'ВСЕГО' ), lastprint=False )
```<!--n:Python Расширенный аналог утилиты wc в Linux:s:0:e:5127-->
<!----><!--2016-06-06 21:49:40-->
## PostgreSQL Репликация кластера
Про настройку репликации мастер-слэйв в *Postgresql* написано много и довольно давно. Выделю лишь [этот](https://habrahabr.ru/post/106872/) пост на Хабре для примера. Важно различать, что репликация и "горячий бэкап" настраиваются и работают отдельно. Репликация - это синхронизация данных серверов слэйвов с мастером в режиме одновременной работы. В случае запуска слэйва после длительной остановки (достаточно 2-3 часов при активных изменениях на мастере) синхронизация с мастером прекращается, поскольку требуемые файлы изменений (транзакций) на мастере уже были удалены и возникает ощибка чтения на слэйве. В этом случае потребуется выполнить полное копирование кластера с мастера на слэйв (выполнить перебазирование) и перезапустить слэйв для старта репликации.

Для избежания этого нужна настройка "горячего резерва" - каталога, где будут храниться все файлы изменений на мастере (WAL-файлы) и откуда они будут считываться в случае прерывания репликации на слэйве.

Включение "горячего" резерва на мастере в *postgresql.conf*.

    archive_mode=on
    archive_command=cp '%p /mnt/disk/home/wal_arc/%f'

Ниже приведен текст скрипта для *Ubuntu* создания зеркала (на слэйве) для базы данных на мастере. 

	#!/bin/bash
	#
	# Создаем кластер для репликации на слэйве
	#
	# На мастере нужно внести правки в postgresql.conf
	#   wal_level = hot_standby
	#   max_wal_senders = 2
	#   wal_keep_segments = 32
	#   checkpoint_segments = 16
	# В pg_hba.conf добавить
	#   host    replication     postgres        0.0.0.0/0            md5
	#
	# На слэйве внести в postgresql.conf
	#   hot_standby = on

	export PGUSER=postgres
	export PGPASSWORD=postgres

	service postgresql stop

	pgconf=/etc/postgresql/9.3/main/postgresql.conf

	cat $pgconf | sed -e 's/^\#\(hot_standby =\) off/\1 on/' > $pgconf.tmp
	[ -s $pgconf.tmp ] && { 
	    mv $pgconf.tmp $pgconf
	    chown postgres:postgres $pgconf
	    chmod 640 $pgconf
	}

	rm -fr /home/pgrepl
	pg_basebackup --host=192.168.0.5 -R -P -D /home/pgrepl || exit 1

	chown -R postgres:postgres /home/pgrepl

	clusterdir="/var/lib/postgresql/9.3/main"
	[ -d "$clusterdir" ] && mv $clusterdir $clusterdir.0

	ln -s /home/pgrepl $clusterdir

	service postgresql start

Базы данных на созданном кластере на слэйве будут доступны только на чтение и синхронно отражать изменения по запросам INSERT - UPDATE - DELETE, выполняемые на мастере. 

В случае восстановления в базу данных на слэйве дампа базы, созданного pg_dump'ом, кроме дампа, созданного с параметрами "Использовать команды Insert", зеркало перестает синхронизироваться с мастером и работает только на чтение. 

В случае создания в кластере слэйва триггер-файла и перевода баз в режим чтение-запись, обратно в режим зеркала (доступ на чтение и синхронизация с мастером) уже нельзя.

После создания зеркала на слэйве нужно создать файл *recovery.conf* для запуска потоковой репликации и восстановления из "горячего" резерва (команда restore_command) одновременно.

    standby_mode='on'
    primary_conninfo='host=pc1 user=postgres password=postgres'
    trigger_file='/home/pg_repl/trigger_file'
    #restore_command='curl -v ftp://pc1/home/wal_arc/%f -o "%p"'
    restore_command='cp /mnt/disk/home/wal_arc/%f -o "%p"'<!--n:PostgreSQL Репликация кластера:s:5217:e:4813-->
<!---->﻿<!--2020-06-06 18:48:27-->
## Раскадровка видео с помощью mplayer
Получение *jpeg*-файлов из видео

    mplayer -vo jpeg film.mov<!--n:Раскадровка видео с помощью mplayer:s:10102:e:185-->
<!----><!--2023-12-16 11:43:22-->
## Запись ISO-образа на флэшку

    dd if="./filename.iso" of="/dev/sdb" status="progress" conv="fsync"<!--n:Запись ISO-образа на флэшку:s:10370:e:157-->
<!----><!--2023-09-30 23:23:09-->
## Python Ресурсивное объединение файлов в каталогах
```python
﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
import fileinput as i
import fnmatch as f

__version__ = '1.0'

STR_HELP = """\
Вызов: python pycat.py <папка> [<файл_масок> | - ]
Объединяет содержимое файлов в один рекурсивно из ПАПКИ по маскам из ФАЙЛА_МАСОК.

ФАЙЛ_МАСОК содержит маски поиска на включение и исключение файлов, разделенных пустой строкой.
Если ФАЙЛ_МАСОК задан как -, читает стандартный ввод, если не задан, подсчитываются все файлы.

Пример файла:
  # включать
  *.c *.cpp
  *.h *.asm
  
  # исключать
  *\.svn\* *\stdafx.h

Примеры использования:
  python pycat.py .               Считать все файлы в текущем каталоге и ниже. 
  python pycat.py тест1 dir       Считать файлы в test1 и ниже, используя файл масок dir."""

REG_COL = '(?:[ \t]*#.*\r?\n?)*((?:[^\r\n]+\r?\n?)+)'
REG_ROW = '([^ \t\r\n]+)'

args = sys.argv[1:]

if (not args):
    print((STR_HELP))
    sys.exit(2)

# файл масок поиска и исключений
_wcfile = []
if (len(args) > 1):
    if (args[1] == '-'):
        wcfile = sys.stdin
    else:
        wcfile = open(args[1])
    _wcfile = re.findall(REG_COL, (wcfile.read()))

res = []
for x in _wcfile:
    res += [re.findall(REG_ROW, x)]

# каталог подсчетов    
os.chdir(args[0])

dd = None
for root, dirs, files in os.walk('.', topdown=False):
    # подпапки
    if (root != dd):
        dd = root
    for name in files:
        curname = os.path.normpath(os.path.join(root, name))
        absname = os.path.join((os.getcwd()), curname)
        if (res):
            p = e = False
            # вхождения
            for x in res[0]:
                p = (f.fnmatch(name, x) or f.fnmatch(curname, x) or f.fnmatch(absname, x))
                if (p):
                    break
            # исключения
            if (len(res) > 1 and p):
                for x in res[1]:
                    e = (f.fnmatch(name, x) or f.fnmatch(curname, x) or f.fnmatch(absname, x))
                    if (e):
                        break
            if (not (p and (not e))):
                #print (('Игнорируем'), (curname), file=sys.stderr)
                continue
        print ((curname), file=sys.stderr)
        print ()
        print (open((curname), encoding='utf-8').read(), file=sys.stdout)
        print ()
        i.close()
```<!--n:Python Ресурсивное объединение файлов:s:10598:e:2862-->
<!----><!--2017-11-22 21:13:41-->
## Конфиг для настройки анонимного ftp-сервера
Конфиг */etc/vsftpd.conf*

    listen=yes
    tcp_wrappers=yes

    write_enable=yes
    anon_root=/
    anon_mkdir_write_enable=yes
    anon_other_write_enable=yes
    anon_upload_enable=yes
    anon_umask=000

    #seccomp_sandbox=NO<!--n:Конфиг для настройки анонимного ftp-сервера:s:13550:e:357-->
<!----><!--2015-12-29 21:14:04-->
## Python Сайт с использованием Django-nonrel фреймворка
В этой статье я хочу рассказать о разработке своего проекта - сайта <a href="http://egaxegax.appspot.com">egaxegax.appspot.com</a>.

Поскольку являюсь большим поклонником языка Python, свой сайт я решил создать на популярном фреймворке Django. Чтобы использовать его на бесплатном хостинге <a href="http://appspot.com">appspot.com</a>, адаптировал код для использования NoSQL версии <a href="https://github.com/django-nonrel">django</a> и платформы <a href="http://appengine.google.com">Google AppEngine</a>.
<br>
<img src="https://habrastorage.org/files/3b2/726/93a/3b272693a25546da95c99d86cc05f854.png" width="128px" />
<br>
Сайт существует уже больше 3 лет с 12-го года. Я использую его как платформу для изучения возможностей <i>django</i> и <i>appengine</i> "вживую". Также интересно изучать статистику по нему в <a href="http://https://www.google.ru/webmasters/">Google Webmasters</a>: поисковые индексы, запросы. Например, для себя я выяснил, что Google индексирует для поиска заголовки title, а не содержимое тегов meta.

Началось все с блога - небольших заметок на программные темы: скрипты, конфиги, примеры использования. Но статьи быстро закончились. А создавать новые в большом объеме не получается. Нужно было что-то большее.

Как-то где-то в Сети я скачал архив файлов с текстами и аккордами песен. Добавил к ним пару десятков своих подборов и решил выложить все на сайт. Всего получилось около 11500 файлов. Вручную столько не загрузить. Для этого я написал скрипт <i>ptext.bat</i>, который преобразует текстовые файлы в дампы для загрузки данных таблиц в <i>GAE DataStore</i>.

Загрузку данных пришлось разделить на несколько этапов из-за ограничений на количество операций записи в сутки в DataStore. В сутки получалось записывать около 700-800 записей (файлов).

После загрузки данных через некоторое время при открытии страницы сайта все чаще стала возникать ошибка <i>503 Server Error: Over Quota</i>. Поизучав логи на сервере, я выяснил, что главными пользователями моего сайта были googlebot и yandexbot, которые обращаются к страницам с интервалом в 2-3 минуты. Ошибка возникает из-за превышения ограничения количества операций в сутки на чтение из DataStore.

Посмотрев документацию и примеры по appengine, я понял, что совсем не использовал модуль cache (а именно memcache). Каждое открытие страницы вызывало обращение к базе данных через QuerySet. В новой схеме результаты выборок из рекордсетов QuerySet я передаю в списки Dictionary, которые сохраняются в кэш и считываются оттуда при повторном обращении. Это решило проблему с быстрым исчерпанием лимита на чтение.

Позже я добавил раздел <i>Фото</i> и <i>Новости</i>. Разделы оформлены как отдельные приложения (apps). Данные хранятся в таблицах DataStore. Раздел <i>Фото</i> также использует хранилище файлов BlobStore. Все приложения используют кэш при выборке данных.

Сейчас по аналогии с разделом <i>Аккорды</i> я заполняю раздел <i>Книги</i>, куда выкладываю тексты электронных книг. Тексты книг я получаю, распаковывая файлы *.epub с помощью скрипта <i>bconv.py</i> из каталога media/scripts. В отличие от текстов песен они намного больше в объеме и не могут быть целиком отображены на странице. Кроме того, возникла проблема с тем, что книга целиком не может быть добавлена в кэш из-за превышения лимита памяти кэша. Для этого я считываю, помещаю в кэш и отображаю их по главам. Правда до конца проблема не решена. Поскольку сейчас в кэш помещается вся книга по главам целиком, при чтении нескольких книг подряд возникает ошибка превышения лимита на чтение. Выход - в чтении и кэшировании только текущей главы, а не всей книги целиком. Но это пока в проекте.

Кому интересно заходите на страницу проекта в репозитории GitHub <a href="http://https://github.com/egaxegax/django-egaxegax">django-egaxegax</a>.<!--n:Python Сайт с использованием Django-nonrel фреймворка:s:14009:e:6321-->
<!----><!--2024-05-25 00:05:09-->
## Astra Linux Special Edition 1.7 Installation disc

Ссылки для загрузки iso-образов дисков установки и разработчика ОС Astra Linux Special Edition (Смоленск) с официального сайта.

[installation-1.7.6.15-15.11.24_17.20.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.6/uu/2/iso/installation-1.7.6.15-15.11.24_17.20.iso)  
[base-1.7.6.15-15.11.24_17.20.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.6/uu/2/iso/base-1.7.6.15-15.11.24_17.20.iso)

[installation-1.7.6.11-26.08.24_17.26.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.6/iso/installation-1.7.6.11-26.08.24_17.26.iso)  
[base-1.7.6.11-26.08.24_17.26.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.6/iso/base-1.7.6.11-26.08.24_17.26.iso)

[installation-1.7.5.16-06.02.24_14.21.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.5/uu/1/iso/installation-1.7.5.16-06.02.24_14.21.iso)  
[base-1.7.5.16-06.02.24_14.21.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.5/uu/1/iso/base-1.7.5.16-06.02.24_14.21.iso)

[installation-1.7.5.9-16.10.23_16.58.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.5/iso/installation-1.7.5.9-16.10.23_16.58.iso)  
[base-1.7.5.9-16.10.23_16.58.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.5/iso/base-1.7.5.9-16.10.23_16.58.iso)

[installation-1.7.4.11-23.06.23_17.13.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.4/uu/1/iso/installation-1.7.4.11-23.06.23_17.13.iso)  
[base-1.7.4.11-23.06.23_17.13.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.4/uu/1/iso/base-1.7.4.11-23.06.23_17.13.iso)<!--n:Astra Linux SE 1.7 Installation Disc:s:20437:e:1696-->
<!----><!--2016-11-15 14:14:32-->
## Сборка boost
Пример строки сборки *boost* под *Visual Studio 10.0*

    bjam link=static variant=debug toolset=msvc-10.0<!--n:Сборка boost:s:22194:e:184-->
<!----><!--2012-11-11 19:42:24-->
## Передача пароля из командной строки ssh
Скрипт для выполнения команд через *ssh* без ввода пароля

    #!/bin/bash
    #
    # script that passes password from stdin to ssh.
    #
    # Copyright (C) 2010 Andre Frimberger <andre OBVIOUS_SIGN frimberger.de>
    #
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.
    #
    
    if [ -n "$SSH_ASKPASS_TMPFILE" ]; then
        cat "$SSH_ASKPASS_TMPFILE"
        exit 0
    elif [ $# -lt 1 ]; then
        echo "Usage: echo password | $0 <ssh command line options>" >&2
        exit 1
    fi
    
    sighandler() {
        rm "$TMP_PWD"
    }
    
    TMP_PWD=$(mktemp)
    chmod 600 "$TMP_PWD"
    trap 'sighandler' SIGHUP SIGINT SIGQUIT SIGABRT SIGKILL SIGALRM SIGTERM
    
    export SSH_ASKPASS=$0
    export SSH_ASKPASS_TMPFILE=$TMP_PWD
    
    [ "$DISPLAY" ] || export DISPLAY=dummydisplay:0
    read password
    echo $password >> "$TMP_PWD"
    
    # use setsid to detach from tty
    exec setsid "$@"
    
    rm "$TMP_PWD"

Пример вызова скрипта как asspass.sh:

    echo 12345678 | ./asspass.sh ssh user@vm1 "hostname;uname;users;groups"<!--n:Передача пароля из командной строки ssh:s:22420:e:1864-->
<!----><!--2024-06-24 01:12:02-->
## xargs Многопоточный запуск команд в bash

Приведу скрипт на *bash*-скрипте для подсчёта количества строк в файлах. 
В качестве задачи используется подсчёт строк с помощью утилиты *wc*. 
Вызов осуществляется внутри функции *runfunc*. 
В качестве запускаемой задачи можно использовать любую доступную в *Linux* утилиту: 
подсчёт размера файла/каталога, контрольной суммы, количества строк, копирование файлов и др.

    #!/bin/bash

    D=${1-}

    runfunc(){
      pushd "$1" >/dev/null
      echo $(ls | wc -l) "files in" $1
      popd >/dev/null
    }

    export -f runfunc

    find $D -type d -name '??*' | xargs -n1 -P10 -I{} bash -c 'runfunc "{}"'<!--n:xargs Многопоточный запуск команд:s:24379:e:1001-->
<!----><!--2024-07-28 11:40:22-->
## Astra Linux Special Edition 1.8 Installation disc
Ссылки для скачивания iso-образов дисков для установки и настройки ОС Astra Linux SE (Smolensk) для ознакомления (ссылки взяты из свободного источника). 

[installation-1.8.1.16-27.12.24_15.22-di.iso](https://home.kataevk.su/Astra%20Linux%20Special%20Edition%201.8.1.16/debian_installer/installation-1.8.1.16-27.12.24_15.22-di.iso)<!--n:Astra Linux SE 1.8 Installation Disc:s:25463:e:521-->
<!----><!--2012-11-12 19:51:55-->
## Используем Samba для скачиваниязакачивания каталогов
Чтобы "скачать" каталог файлов по сети с машины под *Windows* (*Samba*-сервером под *linux*) удобно воспользоваться утилитой *smbclient* из пакета *samba*.
Например.

Список доступных сетевых папок  

    smbclient -L 192.168.0.9 -U Администратор

Подключаемся

    smbclient //192.168.0.9/E$ -U Администратор

В оболочке *Samba* вводим команды для "скачивания" рекурсивно папки в текущий каталог  

    smb:/> recurse
    smb:/> prompt
    smb:/> mget Документы

Аналогично можно закачать папку из текущего каталога 

    smb:/> recurse
    smb:/> prompt
    smb:/> mput home

Текущим путем является текущий путь в терминале, в котором был выполнен *smbclient*<!--n:Используем Samba для скачиваниязакачивания каталогов:s:26044:e:1136-->
<!----><!--2020-04-19 19:36:33-->
## Конфиг привязки DNS-сервера 
    search dom
    nameserver 192.168.0.5<!--n:Конфиг привязки DNS-сервера :s:27300:e:128-->
<!----><!--2025-09-18 12:31:37-->
## git log Вывод списка файлов коммита
Вывод только имен файлов коммита

    git log --name-only --oneline

Включить отображение имён файлов на русском языке

    git config --local core.quotepath false<!--n:git log Список файлов коммита:s:27501:e:331-->
<!---->﻿<!--2020-04-06 11:38:04-->
## Конфиг настройки сервера времени NTP
Конфиг */etc/ntp/ntp.conf*

    # master

    # server srv
    # server 127.127.1.0
    # fudge 127.127.1.0 stratum 10
    # restrict default kod noquery nomodify notrap
    # restrict 127.0.0.1 mask 255.255.255.255 
    # restrict 0.0.0.0 mask 255.255.0.0 
    # logconfig +syncall
    # broadcastdelay 4
    # broadcastclient
    # driftfile /var/lib/ntp/ntp.drift


    # client

    # server srv minpoll 6 maxpoll 10 version 4 prefer
    # server pc1 minpoll 6 maxpoll 10 version 4
    # restrict default
    # logconfig +syncall
    # broadcast 0.0.0.0 minpoll 6 version 4 ttl 127
    # broadcastclient
    # driftfile /var/lib/ntp/ntp.drift

Для запуска мастера (раздающего) нужно раскомментировать что ниже # master, для клиента (синхронизируемого) что ниже клиента и перезапустить сервер

    service ntp restart

или 

    systemctl restart ntpd<!--n:Конфиг настройки сервера времени NTP:s:27904:e:1086-->
<!----><!--2020-12-06 13:45:00-->
## cut Разбиение строки в bash

Разбиваем строку и выделяем подстроку *Солнце стекло* в *bash*

    echo Солнце светит сквозь стекло|cut -d" " -f1,4<!--n:cut Разбиение строки в bash:s:29080:e:268-->
<!---->﻿<!--2021-03-14 23:20:27-->
## Раскадровка видео с помощью mpv
Получение *jpeg*-файлов из видео с заданного времени с помощью плеера [mpv](http://mpv.io)

    mpv -vo image --start=00:11:10 "video.mkv"

[mpv](http://mpv.io) новая версия ***mplayer***.<!--n:Раскадровка видео с помощью mpv:s:29415:e:348-->
<!----><!--2021-05-24 01:01:01-->
## Извлекаем звук из видео с помощью mpv
*mpv* свободный медиаплеер от разработчиков устаревших *mplayer* и *mencoder*.

Извлекаем звуковую дорожку

    mpv file.avi -o file.mp3 --no-video
 
Извлекаем звуковую дорожку по времени начала/конца

    mpv file.avi -o file.mp3 --no-video --start=00:00:11 --end=00:01:01
 
Извлекаем звуковую дорожку по времени длительности
    
    mpv file.avi -o file.mp3 --no-video --start=0 --length=61<!--n:Извлекаем звук из видео с помощью mpv:s:29842:e:654-->
<!----><!--2025-02-09 00:54:01-->
## git Удаление истории репозитория

Очистка всей истории репозитория гита.

Создаем временный бранч

    $ git checkout --orphan temp_branch

Коммит во временный бранч

    $ git add -A
    $ git commit -am "Новый первый коммит"

Удаляем бранч *master*

    $ git branch -D master

Переименовываем временный бранч в *master*

    $ git branch -m master

Принудительно обновляем удаленный репо

    $ git push -f origin master<!--n:git Удаление истории коммитов:s:30585:e:656-->
<!----><!--2016-01-22 21:41:19-->
## Количество файлов в каталоге
Считаем количество файлов в папке

    ls | wc -l<!--n:Количество файлов в каталоге:s:31317:e:169-->
<!----><!--2016-07-23 11:15:01-->
## Python Конвертируем картинку в base64 строку
Скрипт для конвертирования изображений в base64-строку для использования в теге img. 
Тип в data берем из расширения файла.
```python
#!python
# base64 encode image

import sys, os.path
import base64

img = file( sys.argv[1], "rb")
ext = os.path.splitext( sys.argv[1])[1][1:]
print ( "data:image/" + ext + ";base64," + base64.b64encode(img.read()) )
```<!--n:Python Конвертируем картинку в base64 строку:s:31563:e:551-->
<!----><!--2024-05-25 01:05:44-->
## Astra Linux Special Edition 1.6 Installation disc

Ссылки для скачивания iso-образов дисков для установки и настройки ОС Astra Linux SE с официального сайта.

[smolensk-1.6-20.06.2018_15.56.iso](https://dl.astralinux.ru/astra/frozen/1.6_x86-64/1.6.0/iso/smolensk-1.6-20.06.2018_15.56.iso)  
[devel-smolensk-1.6-20.06.2018_15.56.iso](https://dl.astralinux.ru/astra/frozen/1.6_x86-64/1.6.0/iso/devel-smolensk-1.6-20.06.2018_15.56.iso)<!--n:Astra Linux SE 1.6 Installation Disc:s:32209:e:543-->
<!----><!--2022-01-03 01:46:05-->
## Просмотр заряда батареи ноутбука в консоли Linux
Печатаем заряд батареи *BAT1* в ваттах и процентах

    cat /sys/class/power_supply/BAT1/energy_full
    cat /sys/class/power_supply/BAT1/energy_now
    cat /sys/class/power_supply/BAT1/capacity
    cat /sys/class/power_supply/BAT1/status

Вывод

    28390000
    26360000
    92
    Discharging<!--n:Просмотр заряда батареи ноутбука в консоли Linux:s:32812:e:460-->
<!----><!--2013-09-29 20:03:40-->
## PHP Настройка Visual Studio для разработки плагина
Повысить скорость выполнения скриптов, особенно с использованием циклических вычислений, можно, перенеся части кода на язык C и оформив их как плагин PHP. У PHP есть отличный API позволяющий, даже не имея особых навыков программирования на С,создавать модули. Макросы и функции для работы с массивами, строками, входными аргументами уже есть в наличии, а примеры их использования есть в документации и исходном коде.

Создадим свое расширение *myextension* и настроим проект в среде Visual C 9 из пакета разработки Microsoft Visual Studio 9. В VС9 можно собирать модули для php версий 5.2, 5.3, 5.4. Для версии php 5.5 нужно использовать пакет Visual Studio 2012.

Для создания каркаса проекта с в каталоге *ext* в папке исходных кодов php запускаем скрипт *ext_skel* под Linux или *ext_skel_win32.php* под Windows с установленым пакетом Cygwin. 

    ./ext_skel --extname=myextension

В созданной папке *myextension* открываем файл *myextension.dsp* в среде VC9. Открываем окно свойств проекта раскрываем меню *Configuration Properties*. 

Включаем режим отладки в настройках *Linker->Debugging->General Debug Info*, выбираем *Yes (/DEBUG)*.

В настройках *C/C++->General->Debug Information Format* выбираем *Program Database (/ZI)*.

Указываем скрипт запуска во вкладке *Debugging* как *Command* с *..\..\Debug_TS\php.exe* и *Command Arguments* с *-f myextension.php*.

Ставим точку останова, запускаем режим отладки по клавише *F5* и убеждается, что она работает.

![myext3.png] (http://img-fotki.yandex.ru/get/4906/136640652.0/0_c812d_bd2761b5_XL.png)

Все. Теперь сделаем тоже самое, но для среды NetBeans IDE 7.2 под Linux. Для этого в системе должна быть установлена отладочная версия php. Для этого берем исходники с сайта [php.net](http://php.net), например, *php-5.4.9.tar.gz*. Распаковываем и собираем с режимом отладки:

    ./configure --prefix=/usr/local/php54d/ --enable-debug
    make install

После установки запускаем редактор NetBeans, создаем проект *"Приложение на C/C++"* и включаем в него все файлы расширениями *.h и *.c из каталога *<php-src>/ext/myextension*. Открываем вкладку *"Собрать"* в окне свойств проекта. В подпункте *"Тип конфигурации"* указываем *"Динамическая библиотека"*.

В разделе *"Компилятор C"* прописываем пути к инклудам php:

* /usr/local/php54d/include/php
* /usr/local/php54d/include/php/main
* /usr/local/php54d/include/php/Zend
* /usr/local/php54d/include/php/TSRM

В подпункте *"Препроцессорные определения"* указываем *COMPILE_DL_MYEXTENSION=1*.

В настройке *"Компоновщик"->"Вывод"* меняем имя *libmyextension* на *php_myextension*.

Теперь компилируем модуль и копируем его в каталог модулей php. По умолчанию это будет что-то типа */usr/local/php54d/lib64/extensions/debug-non-zts-20100525*. После этого ставим точку останова и запускаем режим отладки. Если все настройки сделаны правильно, должно получиться.

![nb0.png](http://img-fotki.yandex.ru/get/9302/136640652.0/0_c826f_cdce3b6_XL.png)<!--n:PHP Настройка Visual Studio для разработки плагина:s:33381:e:4530-->
<!----><!--2012-11-11 19:36:59-->
## Сменить пароль пользователя passwd без запроса
Сменить пароль пользователя без принудительного ввода пароля
можно так (по непроверенным данным работает только на *RedHat*-совместимых дистрибутивах) 

    echo HELLOWORLD | passwd --stdin<!--n:Сменить пароль пользователя passwd без запроса:s:38015:e:431-->
<!----><!--2020-09-04 16:37:08-->
## Синхронизация каталога по ftp
Синхронизация файлов каталогов с помощью утилиты *ltfp*

    #!/bin/bash
    sudo mkdir -p files
    cd files
    lftp -c mirror ftp://192.168.0.4/home/user/serv
    lftp -c mirror ftp://192.168.0.4/home/user/images
    sudo chmod -R 777 .<!--n:Синхронизация каталога по ftp:s:38551:e:372-->
<!----><!--2013-10-01 20:22:22-->
## Конвертор mp3-файлов в VBR-формат
Конвертор *mp3*-файлов в *VBR*-формат с хорошим качеством и небольшим размером.

Удобен для сжатия *mp3*-файлов с большим битрейтом ( 256, 320 Кб/с ). Использует утилиты *lame* и *id3info*.

    #!/bin/bash
    #
    # Конвертор mp3-файлов в VBR-битрейт
    # Вызов: bash mp3conv [каталог_с_mp3]
    # egax
    
    parse_tag()
    {
      retval=$( echo "$1" | grep -P "$2" | iconv -f CP1251 -t UTF-8 )
      expr match "$retval" ".*:[ \\t]*\( .*\ )"
    }
    
    cd "$1"
    for curfile in *.mp3; do
      tag=$( id3info "$curfile" )

      # берем поля тага
      title=$( parse_tag "$tag" TIT2 )
      artist=$( parse_tag "$tag" TPE1 )
      track=$( parse_tag "$tag" TRCK )
      year=$( parse_tag "$tag" TYER )
      album=$( parse_tag "$tag" TALB )

      mfile="$curfile"
      # новое имя файла $artist - [$track_]$title.mp3
      if [ ! -z "$artist" ] && [ ! -z "$title" ]; then
          if [ ! -z $track ]; then
              [ $track -lt 10  ] && track=0"$track"
              title="$track"_"$title"
          fi
          mfile="$artist"" - "$title".mp3"
      fi

      mdir=1
      # имя папки для новых файлов [$year_]$album
      if [ ! -z "$album" ]; then
          [ -z $year ] || album="$year"_"$album"
          mdir="$album"
      fi

      # создаем папку если не создана
      [ -d "$mdir" ] || mkdir "$mdir"
      mfile="$mdir"/"$mfile"

      # конвертим файл с VBR-битрейдом и копируем таги v2 и v1
      lame --vbr-new -B 192 "$curfile" "$mfile"
      id3cp -2 "$curfile" "$mfile"
      id3cp -1 "$curfile" "$mfile"
    done<!--n:Конвертор mp3-файлов в VBR-формат:s:38999:e:1911-->
<!----><!--2025-09-02 17:35:30-->Подборка различных скриптов на языках Bash, Batch, PHP, Python для различных задач.<!--n:about:s:40990:e:166-->
<!----><!--2013-01-16 20:20:27-->
## Перекодировка файлов из Windows в Linux
При копировании файлов с кириллицей из *Windows* в *Linux* их содержимое может быть не читабельным. Конвертим их, например, в *utf8*:

    #!/bin/bash
    # 
    # Конвертим рекурсивно файлы из кодировки Windows в Юникод из каталога $1
    
    export TMP_F=`mktemp`
    
    trap "rm -f $TMP_F" EXIT
    
    find "$1" -name \*.txt -print|while read x
    do 
        echo $x
        iconv -f cp1251 -t utf8 "$x">$TMP_F && cat $TMP_F > "$x"
    done<!--n:Перекодировка файлов из Windows в Linux:s:41185:e:689-->
<!----><!--2013-07-26 20:30:35-->
## PHP Сборка плагина (extension)
Краткая сводка действий для сборки плагина под PHP 5.2, 5.3, 5.4.

*Сборка под Linux*

PHP должен быть установлен в системе.

    phpize
    ./configure
    make
    make test
    make install (или скопировать вручную php_extension.so)

*Сборка под Windows*

Используем среду Visual Studio 2008.

Настройка php-sdk (поставляется отдельно от дистрибутива php):

    setenv /x86 /xp /release
    cd c:\php-sdk\
    bin\phpsdk_setvars.bat
    bin\phpsdk_buildtree.bat <php_src_dir>

Для PHP 5.2 также нужен win32build (ставится тоже отдельно):

    set INCLUDE=c:\win32build\include

Выставляем переменные окружения Visual Studio:

    c:\Program Files\Microsoft Visual Studio 9.0\VC\bin\vcvars32.bat

Собираем PHP через `configure.js` и `nmake`. В VS2008Express отсутствует компилятор сообщений mc.exe. Его можно взять из VS2010 добавив в Makefile строчку перед "MT = ...":

    MC=C:\Program Files\Microsoft SDKs\Windows\v7.0A\bin\mc.exe 
    MT=C:\Program Files\Microsoft SDKs\Windows\v6.0A\bin\mt.exe

Либо установить Windows SDK.

Инициализируем плагин:

1. php.exe ext_skel_win32.php --extname=myextension --proto=myprototypefile.dat
2. Раскомментарить ARG_ENABLE или ARG_WITH в config.w32

Собираем PHP 5.2 с плагином:

    buildconf.bat
    cscript /nologo configure.js --disable-zts --disable-cgi --disable-fastcgi --disable-path-info-check --disable-bcmath --disable-calendar --disable-com-dotnet --disable-ctype --disable-xmlreader --disable-zlib --disable-xmlwriter --disable-ftp --disable-filter --disable-ctype --disable-com-dotnet --enable-cli --without-xml --without-libxml --without-simplexml --disable-ipv6 --with-EXTENSION[=shared[,PATH]]
    nmake


Сборка PHP 5.3 с плагином:

    buildconf.bat
    cscript /nologo configure.js --disable-all --enable-cli --with-EXTENSION[=shared[,PATH]]
    nmake

Для компиляции через Visual Studio в настройках проекта нужно выставить флаг препроцессора _USE_32BIT_TIME_T.<!--n:PHP Сборка плагина (extension):s:41959:e:2466-->
<!----><!--2020-03-21 16:11:37-->
## git tag push Работа с тагами в git
Добавление тага в локальный репозиторий *git*

    git tag <tag_name>

Добавление в удаленный репозиторий

    git push origin <tag_name>

Удаление тага в локальном и удаленном репозиториях *git*

    git tag -d <tag_name>
    git push origin :refs/tags/<tag_name>

Другой вариант

    git push --delete origin <tag_name>
    git tag -d <tag_name><!--n:git tag delete Удаление тага в git:s:44493:e:556-->
<!----><!--2012-11-11 19:47:05-->
## Создание self-extract архива tar
Скрипт запуска *extract.sh*

    #!/bin/bash
    echo ""
    echo "Self Extracting Installer"
    echo ""
    
    export TMPDIR=`mktemp -d /tmp/selfextract.XXXXXX`
    
    ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0`
    
    tail -n+$ARCHIVE $0 | tar -xzv - -C $TMPDIR
    
    CDIR=`pwd`
    cd $TMPDIR
    ./installer
    
    cd $CDIR
    rm -rf $TMPDIR
    
    exit 0
    
    # newline after
    __ARCHIVE_BELOW__

Пакуем скрипт запуска и архив tar.gz в bundle

    cat extract.sh a.tar.gz > installer.run

Запускаем

    sh installer.run<!--n:Создание self-extract архива tar:s:45120:e:699-->
<!---->﻿<!--2020-04-06 11:44:11-->
## Конфиг настройки сетевых интерфейсов interfaces
Конфиг настройки локальной сети */etc/networking/interfaces*
    
    auto lo eth0 eth1
    iface lo inet loopback
    
    iface eth0 inet static
        address 172.16.0.126
        netmask 255.255.252.0
        gateway 172.16.0.1
        broadcast 172.16.0.255
    
    iface eth1 inet static
        address 172.16.2.126
        netmask 255.255.252.0
        gateway 172.16.2.1
        broadcast 172.16.2.255<!--n:Конфиг настройки сетевых интерфейсов interfaces:s:45889:e:561-->
<!----><!--2014-01-19 19:47:37-->
## Получить сведения о запущенном процессеах
В *Linux* получить список запущенных процессов можно командой

    ps aux

список активных процессов

    top

Узнать, запущен ли конкретный процесс:

    ps -C xterm

В Windows, начиная с windows XP, есть полезная утилита <b>wmic</b>.

Например, узнать путь исполняемого файла процесса можно получить так

    wmic process where (name="cmd.exe") get ExecutablePath<!--n:Получить сведения о запущенном процессеах:s:46554:e:670-->
<!----><!--2016-11-30 20:26:58-->
## Использование ssh через expect с передачей пароля без ввода
Простой скрипт, использующий интерпретатор *expect* для удаленного подключения к хосту по *ssh* без ввода пароля. 
Подключается, выводит информацию о системе через *uname*, закрывает соединение.

    #!/usr/bin/expect -f
    
    set timeout 2
    set USER "agena"
    set HOST "3"
    set PASS "12345678"
    
    spawn ssh $USER@192.168.0.$HOST
    expect {
    "(yes/no)?*" {
    send "yes\r"
    }
    }
    expect "word:"
    send "$PASS\r"
    expect "$*"
    send "uname -a\r"
    expect "$*"
    send "exit\r"
    expect eof<!--n:Использование ssh через expect с передачей пароля без ввода:s:47326:e:816-->
<!----><!--2020-03-22 08:48:27-->
## Кодируем видео из MOV в AVI формат
    mencoder a.mov -o b.avi -oac mp3lame -ovc lavc<!--n:Кодируем видео из MOV в AVI формат:s:48267:e:144-->
<!----><!--2016-10-31 19:39:12-->
## autoconf Сборка 32 битной версии программы на 64 битной версии Linux
Запускаем

    ./configure CC="gcc -m32" CXX="g++ -m32"
     make<!--n:autoconf Сборка 32 битной версии программы на 64 битной версии Linux:s:48491:e:221-->
<!----><!--2018-01-28 08:28:19-->
## Пример настройки dns-сервера bind9
Настроим в локальной сети *192.168.x.x* сервер разрешения имен *dns*. 
Создадим имена *srv*, *db*, *ftp* в домене dom на сервере *192.168.0.1*.

Файл */etc/bind/dom/named.dom*

    $TTL    86400
    @       IN      SOA     srv.dom. root.srv.dom.  (
                                      20180128 ; Serial
                                      28800      ; Refresh
                                      14400      ; Retry
                                      3600000    ; Expire
                                      86400 )    ; Minimum
              IN      NS      srv.dom.

    srv     IN      A     192.168.0.1
    db    IN      A     192.168.2.2
    ftp     IN      A  192.168.0.127

Файл */etc/bind/dom/db.ftp* для настройки короткого имени *ftp* без домена *dom*.

    $TTL    86400
    @       IN      SOA     srv.dom. root.srv.dom.  (
                                      20180128 ; Serial
                                      28800      ; Refresh
                                      14400      ; Retry
                                      3600000    ; Expire
                                      86400 )    ; Minimum
              IN      NS      srv.dom.

          IN      A     192.168.0.127

Прописываем зоны в */etc/bind/named.conf*

    zone "dom" {
        type master;
        file "/etc/bind/dom/named.dom";
    };
    zone "ftp" {
        type master;
        file "/etc/bind/dom/db.ftp";
    };

Запускаем *bind* на сервере *srv*

    sudo /etc/init.d/bind9 restart

Теперь создаем файл */etc/resolv.conf* на всех машинах с которых нужно обращаться по именам

    search dom
    nameserver 192.168.0.1

Пробуем

    ping ftp
    ping ftp.dom
    ping db.dom<!--n:Пример настройки dns-сервера bind9:s:48845:e:1995-->
<!----><!--2019-10-05 22:42:55-->
## Извлекаем звук из видео с помощью mencoder 
Извлекаем и обрезаем дорожку по времени от начала (-ss) с длительностью в сек (-endpos), а также увеличиваем громкость трека га *10 дб* (-af volume=10:0)

    mencoder v.mp4 -ss 56 -endpos 190 -af volume=10:0 -of rawaudio -oac mp3lame -ovc copy -o a.mp3<!--n:Извлекаем звук из видео с помощью mencoder :s:50921:e:457-->
<!----><!--2018-10-29 21:23:47-->
## iframe с autoheight по содержимому
Тэг *iframe* с автовыравниванием по содержимому

    <iframe frameborder=0 width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/">
    </iframe>

Пример

    <iframe frameborder=0 scrolling=no width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/"></iframe><!--n:iframe с autoheight по содержимому:s:51473:e:449-->
<!----><!--2012-11-14 19:59:57-->
## PostgreSQL Работа с индексами
Примеры как работать с индексами таблиц для ускорения выборки данных. Для примера возьмем таблицу "grade" (данные по классам учеников школ) с 2,5 млн. записей. Тесты проводились на PostgreSQL 7.4.1.

Структура таблицы и индекса:

    ::::sql
    CREATE TABLE "grade" 
    (
      "id_school" integer,
      "id_class" integer,
      "sum_count" integer,
      "year_num" integer,
      "male_ratio" double precision,
      "avg_score" double precision
    )
    WITH OIDS;
     
    CREATE INDEX "grade_index" 
      ON "grade" 
      USING btree
      ("id_class", "id_school", "sum_count", "year_num", "male_ratio");

Запросы к таблице. Работает или нет индекс определяем по `explain`:

    ::::sql
    --индекс работает - время < 0.5 сек - ~ 300 тыс. строк
    select * from "grade" where "id_class"=14 and "id_school"=1 and "sum_count"=14;
    --индекс не работает - время > 2 сек - ~ 600 тыс. строк
    select * from "grade" where "id_class"=14 and "id_school"=1;
    select * from "grade" where "id_class"=14;
     
    --индекс работает
    select * from "grade" where 
        (id_class=14 and id_school=14 and year_num>0 and sum_count=14) or
        (id_class=1 and id_school=1 and year_num>2000 and sum_count=14) or
        (id_class=14 and id_school=2 and year_num>2000 and sum_count=14) 
    and male_ratio between 1 and 200 limit 100;
    
    --индекс не работает
    select * from "grade" where 
        (id_class=14 and id_school=14 and year_num>0 and sum_count>0);

Индекс работает на равно (=) когда число полей в запросе больше половины числа полей в индексе. Чувствителен к операциям множеств (>,<,BETWEEN) и конструкции IN (ее нужно заменить на комбинацию с OR).<!--n:PostgreSQL Работа с индексами:s:51994:e:2214-->
