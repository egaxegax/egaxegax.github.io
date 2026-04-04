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
```<!--n:Примеры shell-сценариев/Python Расширенный аналог утилиты wc в Linux:s:0:e:5127-->
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
    restore_command='cp /mnt/disk/home/wal_arc/%f -o "%p"'<!--n:Примеры shell-сценариев/PostgreSQL Репликация кластера:s:5257:e:4813-->
<!---->﻿<!--2020-06-06 18:48:27-->
## Раскадровка видео с помощью mplayer
Получение *jpeg*-файлов из видео

    mplayer -vo jpeg film.mov<!--n:Примеры shell-сценариев/Раскадровка видео с помощью mplayer:s:10182:e:185-->
<!----><!--2023-12-16 11:43:22-->
## Запись ISO-образа на флэшку

    dd if="./filename.iso" of="/dev/sdb" status="progress" conv="fsync"<!--n:Примеры shell-сценариев/Запись ISO-образа на флэшку:s:10490:e:157-->
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
```<!--n:Примеры shell-сценариев/Python Ресурсивное объединение файлов:s:10758:e:2862-->
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

    #seccomp_sandbox=NO<!--n:Примеры shell-сценариев/Конфиг для настройки анонимного ftp-сервера:s:13750:e:357-->
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

Кому интересно заходите на страницу проекта в репозитории GitHub <a href="http://https://github.com/egaxegax/django-egaxegax">django-egaxegax</a>.<!--n:Примеры shell-сценариев/Python Сайт с использованием Django-nonrel фреймворка:s:14249:e:6321-->
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
[base-1.7.4.11-23.06.23_17.13.iso](https://dl.astralinux.ru/astra/frozen/1.7_x86-64/1.7.4/uu/1/iso/base-1.7.4.11-23.06.23_17.13.iso)<!--n:Примеры shell-сценариев/Astra Linux SE 1.7 Installation Disc:s:20717:e:1696-->
<!----><!--2016-11-15 14:14:32-->
## Сборка boost
Пример строки сборки *boost* под *Visual Studio 10.0*

    bjam link=static variant=debug toolset=msvc-10.0<!--n:Примеры shell-сценариев/Сборка boost:s:22514:e:184-->
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

    echo 12345678 | ./asspass.sh ssh user@vm1 "hostname;uname;users;groups"<!--n:Примеры shell-сценариев/Передача пароля из командной строки ssh:s:22780:e:1864-->
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

    find $D -type d -name '??*' | xargs -n1 -P10 -I{} bash -c 'runfunc "{}"'<!--n:Примеры shell-сценариев/xargs Многопоточный запуск команд:s:24779:e:1001-->
<!----><!--2024-07-28 11:40:22-->
## Astra Linux Special Edition 1.8 Installation disc
Ссылки для скачивания iso-образов дисков для установки и настройки ОС Astra Linux SE (Smolensk) для ознакомления (ссылки взяты из свободного источника). 

[installation-1.8.1.16-27.12.24_15.22-di.iso](https://home.kataevk.su/Astra%20Linux%20Special%20Edition%201.8.1.16/debian_installer/installation-1.8.1.16-27.12.24_15.22-di.iso)<!--n:Примеры shell-сценариев/Astra Linux SE 1.8 Installation Disc:s:25903:e:521-->
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

Текущим путем является текущий путь в терминале, в котором был выполнен *smbclient*<!--n:Примеры shell-сценариев/Используем Samba для скачиваниязакачивания каталогов:s:26524:e:1136-->
<!----><!--2025-09-18 12:31:37-->
## git log Вывод списка файлов коммита
Вывод только имен файлов коммита

    git log --name-only --oneline

Включить отображение имён файлов на русском языке

    git config --local core.quotepath false<!--n:Примеры shell-сценариев/git log Список файлов коммита:s:27820:e:331-->
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

    systemctl restart ntpd<!--n:Примеры shell-сценариев/Конфиг настройки сервера времени NTP:s:28263:e:1086-->
<!----><!--2020-12-06 13:45:00-->
## cut Разбиение строки в bash

Разбиваем строку и выделяем подстроку *Солнце стекло* в *bash*

    echo Солнце светит сквозь стекло|cut -d" " -f1,4<!--n:Примеры shell-сценариев/cut Разбиение строки в bash:s:29479:e:268-->
<!---->﻿<!--2021-03-14 23:20:27-->
## Раскадровка видео с помощью mpv
Получение *jpeg*-файлов из видео с заданного времени с помощью плеера [mpv](http://mpv.io)

    mpv -vo image --start=00:11:10 "video.mkv"

[mpv](http://mpv.io) новая версия ***mplayer***.<!--n:Примеры shell-сценариев/Раскадровка видео с помощью mpv:s:29854:e:348-->
<!----><!--2021-05-24 01:01:01-->
## Извлекаем звук из видео с помощью mpv
*mpv* свободный медиаплеер от разработчиков устаревших *mplayer* и *mencoder*.

Извлекаем звуковую дорожку

    mpv file.avi -o file.mp3 --no-video
 
Извлекаем звуковую дорожку по времени начала/конца

    mpv file.avi -o file.mp3 --no-video --start=00:00:11 --end=00:01:01
 
Извлекаем звуковую дорожку по времени длительности
    
    mpv file.avi -o file.mp3 --no-video --start=0 --length=61<!--n:Примеры shell-сценариев/Извлекаем звук из видео с помощью mpv:s:30321:e:654-->
<!----><!--2019-10-05 22:42:55-->
## Извлекаем звук из видео с помощью mencoder 
Извлекаем и обрезаем дорожку по времени от начала (-ss) с длительностью в сек (-endpos), а также увеличиваем громкость трека га *10 дб* (-af volume=10:0)

    mencoder v.mp4 -ss 56 -endpos 190 -af volume=10:0 -of rawaudio -oac mp3lame -ovc copy -o a.mp3<!--n:Примеры shell-сценариев/Извлекаем звук из видео с помощью mencoder:s:31104:e:457-->
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

    $ git push -f origin master<!--n:Примеры shell-сценариев/git Удаление истории коммитов:s:31695:e:656-->
<!----><!--2016-01-22 21:41:19-->
## Количество файлов в каталоге
Считаем количество файлов в папке

    ls | wc -l<!--n:Примеры shell-сценариев/Количество файлов в каталоге:s:32467:e:169-->
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
```<!--n:Примеры shell-сценариев/Python Конвертируем картинку в base64 строку:s:32753:e:551-->
<!----><!--2024-05-25 01:05:44-->
## Astra Linux Special Edition 1.6 Installation disc

Ссылки для скачивания iso-образов дисков для установки и настройки ОС Astra Linux SE с официального сайта.

[smolensk-1.6-20.06.2018_15.56.iso](https://dl.astralinux.ru/astra/frozen/1.6_x86-64/1.6.0/iso/smolensk-1.6-20.06.2018_15.56.iso)  
[devel-smolensk-1.6-20.06.2018_15.56.iso](https://dl.astralinux.ru/astra/frozen/1.6_x86-64/1.6.0/iso/devel-smolensk-1.6-20.06.2018_15.56.iso)<!--n:Примеры shell-сценариев/Astra Linux SE 1.6 Installation Disc:s:33439:e:543-->
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
    Discharging<!--n:Примеры shell-сценариев/Просмотр заряда батареи ноутбука в консоли Linux:s:34082:e:460-->
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

![nb0.png](http://img-fotki.yandex.ru/get/9302/136640652.0/0_c826f_cdce3b6_XL.png)<!--n:Примеры shell-сценариев/PHP Настройка Visual Studio для разработки плагина:s:34691:e:4530-->
<!----><!--2012-11-11 19:36:59-->
## Сменить пароль пользователя passwd без запроса
Сменить пароль пользователя без принудительного ввода пароля
можно так (по непроверенным данным работает только на *RedHat*-совместимых дистрибутивах) 

    echo HELLOWORLD | passwd --stdin<!--n:Примеры shell-сценариев/Сменить пароль пользователя passwd без запроса:s:39365:e:431-->
<!----><!--2020-09-04 16:37:08-->
## Синхронизация каталога по ftp
Синхронизация файлов каталогов с помощью утилиты *ltfp*

    #!/bin/bash
    sudo mkdir -p files
    cd files
    lftp -c mirror ftp://192.168.0.4/home/user/serv
    lftp -c mirror ftp://192.168.0.4/home/user/images
    sudo chmod -R 777 .<!--n:Примеры shell-сценариев/Синхронизация каталога по ftp:s:39941:e:372-->
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
    done<!--n:Примеры shell-сценариев/Конвертор mp3-файлов в VBR-формат:s:40429:e:1911-->
<!----><!--2025-09-02 17:35:30-->Подборка различных скриптов на языках Bash, Batch, PHP, Python для различных задач.<!--n:Примеры shell-сценариев/about:s:42460:e:166-->
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
    done<!--n:Примеры shell-сценариев/Перекодировка файлов из Windows в Linux:s:42695:e:689-->
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

Для компиляции через Visual Studio в настройках проекта нужно выставить флаг препроцессора _USE_32BIT_TIME_T.<!--n:Примеры shell-сценариев/PHP Сборка плагина (extension):s:43509:e:2466-->
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
    git tag -d <tag_name><!--n:Примеры shell-сценариев/git tag delete Удаление тага в git:s:46083:e:556-->
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

    sh installer.run<!--n:Примеры shell-сценариев/Создание self-extract архива tar:s:46750:e:699-->
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
        broadcast 172.16.2.255<!--n:Примеры shell-сценариев/Конфиг настройки сетевых интерфейсов interfaces:s:47559:e:561-->
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

    wmic process where (name="cmd.exe") get ExecutablePath<!--n:Примеры shell-сценариев/Получить сведения о запущенном процессеах:s:48264:e:670-->
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
    expect eof<!--n:Примеры shell-сценариев/Использование ssh через expect с передачей пароля без ввода:s:49076:e:816-->
<!----><!--2020-03-22 08:48:27-->
## Кодируем видео из MOV в AVI формат
    mencoder a.mov -o b.avi -oac mp3lame -ovc lavc<!--n:Примеры shell-сценариев/Кодируем видео из MOV в AVI формат:s:50057:e:144-->
<!----><!--2016-10-31 19:39:12-->
## autoconf Сборка 32 битной версии программы на 64 битной версии Linux
Запускаем

    ./configure CC="gcc -m32" CXX="g++ -m32"
     make<!--n:Примеры shell-сценариев/autoconf Сборка 32 битной версии программы на 64 битной версии Linux:s:50321:e:221-->
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
    ping db.dom<!--n:Примеры shell-сценариев/Пример настройки dns-сервера bind9:s:50715:e:1995-->
<!----><!--2020-04-19 19:36:33-->
## Конфиг привязки DNS-сервера 
    search dom
    nameserver 192.168.0.5<!--n:Примеры shell-сценариев/Конфиг привязки DNS-сервера:s:52831:e:128-->
<!----><!--2018-10-29 21:23:47-->
## iframe с autoheight по содержимому
Тэг *iframe* с автовыравниванием по содержимому

    <iframe frameborder=0 width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/">
    </iframe>

Пример

    <iframe frameborder=0 scrolling=no width="100%" height="this.height=this.contentWindow.document.body.scrollHeight" src="/"></iframe><!--n:Примеры shell-сценариев/iframe с autoheight по содержимому:s:53071:e:449-->
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

Индекс работает на равно (=) когда число полей в запросе больше половины числа полей в индексе. Чувствителен к операциям множеств (>,<,BETWEEN) и конструкции IN (ее нужно заменить на комбинацию с OR).<!--n:Примеры shell-сценариев/PostgreSQL Работа с индексами:s:53632:e:2214-->
<!----><!--2019-05-11 11:44:53-->
## Запрет вывода сообщений об обновлении *Firefox 63* и выше
Активировать групповую политику для браузера в реестре
  
    HKEY_LOCAL_MACHINE\ Software\ Policies\ Mozilla\ Firefox 
    DisableAppUpdate = DWORD:00000001<!--n:Сценарии для Windows/Запрет вывода сообщений об обновлении Firefox 63 и выше:s:55956:e:338-->
<!---->﻿<!--2020-04-19 17:52:23-->
## Синхронизация времени под Windows
Открыть реестр командой *regedit* 

    HKLM\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpClient

и выставить значение интервала синхронизации в поле *SpecialPollInterval*. 
По умолчанию он равен *604800* сек (раз в неделю).

В консоли выполнить команду

    net time \\192.168.0.5 /set /y

где *192.168.0.5* адрес машины где настроен сервер времени.<!--n:Сценарии для Windows/Синхронизация времени под Windows:s:56443:e:620-->
<!----><!--2019-05-11 11:40:46-->
## Удаление интернет-браузера из запланированных задач *Windows*
Иногда вредоносные скрипты прописывают запуски программ в системном планировщике заданий (например, *Яндекс Browser*). 
Чтобы отключить автоматический запуск программы, нужно запустить планировщик *Windows* 

*Панель инструментов* -> *Администрирование* -> *Планировщик заданий* -> *Библиотека планировщика заданий*

Найти там строку с названием программы (*Яндекс*-браузером или *Microsoft OneDrive*) и удалить ее.<!--n:Сценарии для Windows/Удаление интернет-браузера из запланированных задач Windows:s:57175:e:864-->
<!----><!--2019-07-20 22:30:54-->
## Запрет вывода push-сообщений в *Firefox 44* и выше
В настройках браузера по адресу *about:config* отключить опции

    dom.push.enabled              false
    dom.webnotifications.enabled  false<!--n:Сценарии для Windows/Запрет вывода push-сообщений в Firefox 44 и выше:s:58200:e:299-->
<!---->﻿<!--2020-04-14 09:03:23-->
## Очистка от устаревших обновлений
Чтобы освободить место на диске можно почистить каталог где лежат скаченные и недокаченные обновления *Windows*

*%windir%\SoftwareDistribution\Download*

Очистить папку *WinSxS* от устаревших обновлений

    Dism.exe /online /cleanup-image /AnalyzeComponentStore
    Dism.exe /online /cleanup-image /StartComponentCleanup<!--n:Сценарии для Windows/Очистка от устаревших обновлений:s:58630:e:547-->
<!----><!--2017-02-18 14:28:56-->
## Строка распознавания User-Agent браузера
*iPad 3G*

    Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 
    Mobile/9B206 Safari/7534.48.3

Параметр в *about:config* для изменения **general.useragent.override**<!--n:Сценарии для Windows/Строка распознавания User-Agent браузера:s:59294:e:345-->
<!----><!--2025-09-02 17:35:30-->Советы по настройке и примеры скриптов для работы в ОС Windows.<!--n:Сценарии для Windows/about:s:59762:e:141-->
<!----><!--2024-01-01 22:11:49-->
## Сайт на GH-Pages платформе egaxegax.github.io
Хочу рассказать о своём новом (хотя существует уже почти *3* года) сайте [egaxegax.github.io](//egaxegax.github.io),
после закрытия предыдущего сайта [egaxegax.appspot.com](//egaxegax.appspot.com) на хостинге [Google App Engine](appengine.google.com) в начале 2021 года.
О нём я писал в статье [Cайт на Django-nonrel на платформе Google App Engine для Python](//habr.com/ru/articles/274431/).
Эта статья рассчитана на тех, кто хочет узнать или получить простой сайт с возможностью добавления и правки контента на основе *markdown*-постов.

Сайт [egaxegax.appspot.com](//egaxegax.appspot.com) просуществовал *10* лет на хостинге *GAE*.
Но был закрыт вместе с бесплатным доступом к *GAE* после изменений политики *Google*.
В начале *2020* года *Google* прислал уведомление на почту, что к концу года мне нужно выбрать 
один из платных планов хостинга (от *300$* в месяц), а бесплатный доступ будет закрыт. 
И я стал готовиться к переезду с *GAE*, забэкапив содержимое сайта. 

У меня уже был проект [dbcartajs](//dbcartajs.github.io) на *github* и сайт к нему на платформе *Github Pages*.
И я решил перенести всё содержимое старого сайта в репозиторий *GitHub*, открыв к нему доступ по схеме *GitHub Pages*. 
Для этого текстовый бекап базы данных с содержимым старого сайта я разбил на маленькие *.txt* файлы c *html*-содержимым для каждой строчки из таблицы, то есть для каждого поста.
*Python*-код моделей и вью старого сайта, написанного для фреймфорка *Django-nonrel* я переписал на языках *JavaScript* и *HTML*, 
упростив код и отказавшись от онлайн-редактирования содержимого сайта.
Позже я перевёл *.txt*-файлы в *markdown*-формат *.md* для отображения страниц в репозитории также как на сайте, но отказался от использования шаблонов *Jekyll*, 
создав в корне проекта файл *.nojekyll*, поскольку компиляция им *.md* файлов для сборки сайта на *Github Pages* (после *git push* в *master*) идет очень долго. 
*GitHub* автоматически конвертит *.md* файлы и отображает как *html* на страницах репозитория. 
В большинстве репозиториев есть хотя бы один *README.md* файл, у меня в проекте *.md* файлов оказалось больше *30,000*.

В новой схеме для управления содержимым я использую индексные файлы *index.js*, содержащие список всех *.md* файлов с содержимым каждого раздела сайта.
Для переиндексации после добавления или удаления новых *.md* файлов контента используется *python*-скрипт *update.py*.

Новый сайт разделен на разделы: *books* (*Книги*), *foto* (*Фото*), *posts* (*Заметки*), *songs* (*Аккорды*), *vesti* (*Записки*) 
и *dbcartajs* (*Карты*, как символьная ссылка на папку проекта).
Разделы являются подкаталогами после клонирования проекта из [репозитория](//github.com/egaxegax) *github* на диск.

Подробная инструкция о том, как пользоваться сайтом, есть в *README*-файле [описания проекта](//github.com/egaxegax/egaxegax.github.io#readme).<!--n:Сайт для блогов и карт/Создание статического сайта для блогов:s:59964:e:4618-->
<!----><!--2013-09-20 21:28:19-->
## Карта Московского метро на Canvas
Идея попробовать нарисовать карту появилась после просмотра карты метро в Википедии в [формате SVG](http://upload.wikimedia.org/wikipedia/commons/f/f3/Moscow_metro_map_ru_sb.svg). В Firefox она открывается долго, к тому же при разрешении 1600x1300 она не вмещается в экран, а скроллинг по ней работает тоже очень долго. Стало интересно, а в Canvas она тоже будет тормозить? Решил нарисовать свою версию [карты метро](http://dbcartajs.appspot.com/mosmetro.html) в качестве очередного демо для проекта [dbCartajs](http://dbcartajs.appspot.com). 

![mosmetro.png] (http://img-fotki.yandex.ru/get/9328/136640652.0/0_c6660_9d3ca715_XL.png "Moscow Metro")

Canvas поддерживает далеко не все возможности, которые есть в SVG. Например, как выяснилось, он частично поддерживает рисование пунктирных линий: метод setDashLine поддерживает только Chrome, а Firefox использует свое свойство mozDash. Зато Canvas поддерживает Bezier Curve для отрисовки плавных изгибов.
Я добавил возможность использования метода bezierCurveTo в dbCartajs, если в тройке координат третьим параметром идет символ 'Q', например, для объекта с координатами [[1,1,'Q'],[2,2,'Q'],[3,3,'Q'],[4,4,'Q'],[5,5,'Q'],[6,6,'Q']] метод bezierCurveTo будет вызван 2 раза. Также добавил проверку для поддержки Dash Line, который можно задать как свойство dash в mopt. 

Пиксельные координаты линий, станций, каналов, рек, ж/д путей переведены в градусы с долготой и широтой. Новые координаты объектов сохранены в файле mosmetro.js.

Из станций сформирован выпадающий список. Выбор станции в нем центрирует ее на карте.

В целом получается, что в Canvas карта отрисовывается намного быстрее, чем в SVG. Особенно это заметно на планшете.<!--n:Сайт для блогов и карт/Карта Московского метро на Canvas:s:64720:e:2743-->
<!----><!--2014-03-02 18:53:53-->
## Звездное Небо на Canvas. Созвездия 
Продолжение темы, начатой в предыдущей [статье](http://habrahabr.ru/post/189692/). Идеей к ее развитию послужило прочтение статьи на Хабре &laquo;[LibCanvas: На пути к звёздам](http://habrahabr.ru/post/181554/)&raquo;, где описывается реализация планетария на Canvas с выводом созвездий и планет в азимутальной системе координат. В посте автор дает [ссылку](http://astrokot.ru/planetarium/js/modules/Stars.js) на базу данных звезд и созвездий, которой я любезно воспользовался. Файл содержит координаты прямого восхождения (Right Ascension, в часах)  и склонения (Declination, в градусах) звезд, точек созвездий и их названий. Я перевел их в радианы и сохранил в файл [constellations.js](http://dbcartajs.appspot.com/data/constellations.js) для своего "звездного" проекта [Starry Sky](http://dbcartajs.appspot.com/starry.html).

<img src="http://habrastorage.org/files/c3c/22d/7a5/c3c22d7a5767401fa36afda82471c12e.png" alt="Starry Sky" width="900px"/>

## Разница

Сравнив результаты я заметил, что в оригинальном планетарии все выглядит зеркально наоборот. То есть звезды выведены на внешнюю сторону сферы, а у меня - на внутреннюю. Я решил воспользоваться другим планетарием как эталоном. Для этой цели выбрал проект ["Звезды"](http://maps.mail.ru/stars.html) на Картах@Mail.ru. Оказалось, что правильный вариант отображения - на внутренней стороне звездной сферы. Это видно на рисунке (время 2/3/2014 17:2:0, точка наблюдения - д 37,ш 55 Москва).

![planets-diff](http://habrastorage.org/files/723/750/002/7237500027db40eca6224d9659344f2a.png)

## Что нового

Помимо созвездий в своем планетарии [Starry Sky](http://dbcartajs.appspot.com/starry.html) я добавил вывод информации по звездам, планетам, точкам космических аппаратов при наведении мышью на них (активные области). 
Для звезд выводится номер из каталога Henry Draper'a (HD).

Кроме звезд и планет на карте добавлены три космических аппарата из группировки ГЛОНАСС. Данные взяты с ресурса [celestrak.com](http://celestrak.com) и сохранены в файле [tledata.js](http://dbcartajs.appspot.com/data/tledata.js). Всего в группировке 28 аппаратов, но для наглядности выведены 3 первых по списку. Для расчета орбит и положений КА я использовал модуль [satellite-js](https://github.com/shashwatak/satellite-js).

Изменение масштаба карты привязано к изменению высоты над поверхностью Земли. Размер звездной сферы зафиксирован поскольку в противном случае теряется реалистичность изображения, кода края небесной сферы становятся меньше краев карты. В идеале хотелось бы создать эффект бесконечной Вселенной как в Celestia с удалением и приближением звезд и планет.

Включать или выключать слои (группы объектов) теперь можно через отдельный список layers...

* cntlines - линии созвездий,
* cntpos - названия созвездий,
* star - звезды,
* sun Солнце,
* moon - Луна,
* planet - планеты,
* earth - Земля,
* sattrac - орбиты КА,
* satsurface - подспутниковые точки КА,
* sattrace - проекции эфемерид КА на Землю,
* satsector - поля зрений КА (18 градусов),
* satpos - точка КА на орбите,
* terminator - ночная зона.

## Результаты

Главной проблемой планетария с [astrokot.ru](http://astrokot.ru/planetarium/dev/planetarium.html), как пишет автор, является медлительность программы. Я замерил времена в профайлере Firefox 19. В Planetarium - 1168 ms, в Starry - 608 ms. Действительно медленно, в Starry объектов больше, а время в 2 раза меньше. Видимо в циклах используются лишние вычисления, которые замедляют вывод.

Исследуя звездные алгоритмы для своего проекта, я пытаюсь максимально упрощать вычисления и код, чтобы они были понятны и наглядны. Изучая коды других проектов (Celestia, Stellarium, libastro), особенно на WebGL, очень трудно разобраться, какие используются формулы и как они работают. Для себя я выделил пока два проекта - libnova и Marble - код которых  понятен и максимально пригоден для портирования в другие среды, например в JS.<!--n:Сайт для блогов и карт/Звездное небо на Canvas. Созвездия:s:67585:e:6210-->
<!----><!--2014-04-06 19:44:46-->
## gdal_translate и gdalwarp для перепроицирования изображений
В составе проекта [GDAL](http://gdal.org) есть полезные утилиты для работы с изображениями через консоль

* gdal_translate
* gdalwarp

В среде *Windows* они доступны, например, в сборке программ [MS4W](http://www.ms4w.com/download.html#download).

Для своего проекта *dbcartajs* мне потребовались изображения для разных проекций. Изображения я хочу вывести на канвас вместе с векторными данными. 
Для этого цели из программы *Orbitron* я позаимствовал картинку с плоской картой Земли в небольшом разрешении.

![worldmap.jpg](http://img-fotki.yandex.ru/get/9802/136640652.0/0_e0110_1d7bbe1b_XL.jpg)

Она отлично подходит для экспериментов, но как быть с другими проекциями - *меркатор*, *сфера*? 
Я нашел несколько картинок в разных проекциях, но все они оказались в разных цветовых сочетаниях и разрешениях, поэтому решил попробовать самостоятельно преобразовать исходную картинку с помощью утилит *gdal*, используя их описание и примеры.

Сначала, преобразуем исходную картинку в формат *tiff* - родной формат *gdal* - и задаем координаты привязки изображения.

    gdal_translate -of Gtiff -co "TFW=YES" -a_ullr -180 90 180 -90 worldmap.png worldmap.tif

Для проекции *Меркатора* нужно ограничить размеры на полюсах (80-85 градусов).

    gdal_translate -of Gtiff -projwin -180 84 180 -84 worldmap.tif worldmap-1.tif

Теперь формируем изображение в проекции Меркатора в формате *tiff*.

    gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857 worldmap-1.tif worldmap-merc.tif 

Браузер не работают с tiff, поэтому переводим его в *jpeg*.

    gdal_translate -of JPEG worldmap-merc.tif worldmap-merc.jpg

Вот результат

![worldmap-merc.jpg](http://img-fotki.yandex.ru/get/9802/136640652.0/0_e0111_1a993774_XL.jpg)

Аналогично получаем картинки для других проекций, например *ortho*.

    gdalwarp -s_srs EPSG:4326 -t_srs "+proj=ortho +lon_0=0 +lat_0=0" worldmap-1.tif worldmap-ortho.tif
    gdal_translate -of JPEG worldmap-ortho.tif worldmap-ortho.jpg

![worldmap-ortho.jpg](http://img-fotki.yandex.ru/get/9816/136640652.0/0_e0112_e8d7e76f_L.jpg)<!--n:Сайт для блогов и карт/gdal_translate и gdalwarp для перепроицирования изображений:s:73918:e:3051-->
<!----><!--2013-07-18 19:29:49-->
## Идея
Решил написать пост о популярном нынче <i>Canvas</i> из <i>HTML5</i> и о своем проекте <i>dbCartajs</i>, его использующем. Почему <i>Canvas</i>? Немного истории. Прежде для создания изображений, иллюстрирующих различные расчетные модели (например, вывод окружности по радиусу и центру в координатах, вывод многоугольника с количеством вершин N и площадью S, вывод окружности на сферу и т.д.), я и мои коллеги по работе в институте использовали различные элементы управления из разных сред разработки: <i>PictureBox</i> их <i>VB6</i>, <i>QPainter</i> и <i>QCanvas</i> из <i>Qt</i>, <i>Canvas</i> из <i>Tk</i> и, наконец, создание изображений по <i>mapfile</i> из <i>MapServer</i>. Позже после знакомства с возможностями <i>HTML5</i> я решил перейти на использование <i>Canvas</i> и <i>Web</i>-разработку с <i>JavaScript</i>. Удобно - для отладки и разработки нужен лишь браузер. Собравшись с силами и вооружившись документацией от <i>W3C</i>, я переписал часть функционала компонентов, которые мы используем в работе, на <i>JavaScript</i>, оформив это в проект <i>dbCartajs</i> на <i>GitHub</i>. Код реализован в виде объекта <i>dbCarta</i>, чтобы использовать его как виджет на страницах без копирования частей исходного кода.

![Скриншот виджета с dbCarta](http://img-fotki.yandex.ru/get/9064/136640652.0/0_b999b_feccc6d_L.jpg "Чемпионат Мира по футболу 2014 пройдет в Бразилии")
<br>
Виджет с <i>dbCarta</i>.

Собственно идейно <i>dbCartajs</i> портирован из проекта <i>dbCarta</i> на [googlecode](http://dbcarta.googlecode.com), реализованном на <i>Python</i> и <i>Tkinter</i>.

## Как это работает

<i>dbCartajs</i> использует <i>Canvas</i> для вывода объектов по координатам (долгота, широта в градусах) или пойнтам (points). В проект включена библиотека <i>Proj4js</i>, реализующая пересчеты картографических проекций. Из нее на использование настроены несколько проекций - это сферические <i>nsper</i>, <i>ortho</i>, <i>laea</i> и <i>меркатор</i> (как у популярного <i>Google Maps</i> - <i>Google Mercator</i>). По умолчанию используется холст с соотношением сторон ширина-высота 2:1, что соответствует плоской проекции <i>longlat</i> из <i>Proj4js</i>. Если <i>proj4js-combined.js</i> подгружен, то доступны другие проекции через интерфейсы <i>changeProject</i> или initProj объекта <i>dbCarta</i>.

Конечно, не все возможности <i>Canvas</i> реализованы в <i>dbCartajs</i>, но некоторым я постарался уделить внимание. Первое, это шрифты. При масштабировании они не меняются. Второе, это использование метода <i>isPointInPath</i>, позволяющего реализовать аналог использования элементов <i>MAP</i>, <i>AREA</i> и <i>IMG</i>. И третье, это возможность совмещения объектов из разных проекций. В демо StarrySky для вывода границ Земли, контуров материков используется сферическая проекция nsper, для вывода звезд, орбит космических аппаратов - плоская проекция <i>longlat</i>. Для смены проекций используются методы <i>initProj</i> (с указанием параметров проекции для <i>Proj4js</i>) или <i>changeProject</i> (без параметров).

![Скриншот с демо StarrySky](http://img-fotki.yandex.ru/get/9494/136640652.0/0_b9db5_bda38590_L.jpg "Совмещение проекций в StarrySky")
<br>
Совмещение проекций в <i>StarrySky</i>.

## Про управление

Перемещение по карте доступно по клику (по клику центрируется точка в пределах карты). Масштабирование карты осуществляется через интерфейс <i>scaleCarta</i> или по кнопкам <i>+/-</i>, расположенным справа. В сферических проекциях вращение глобуса осуществляется через интерфейс <i>initProj</i>.

## Где посмотреть

Примеры проекта можно посмотреть на сaйте [dbcartajs.appspot.com](http://dbcartajs.appspot.com). Исходники доступны в [GitHub](http://github.com/egaxegax/dbcartajs).<!--n:Сайт для блогов и карт/Идея создания проекта:s:77126:e:5817-->
<!----><!--2013-11-24 17:34:57-->
## Схема пригородного движения жд сообщения Москвы и МО
Ещё одна схема движения железнодорожного транспорта с использованием возможностей Canvas и dbCartajs. 
![mosrails](http://img-fotki.yandex.ru/get/9309/136640652.0/0_d0765_21a54280_XL.png)

В оригинале она называется Moscow Underground and Commuter Rail Map, её можно видеть в тамбурах подмосковных электричек. Изначально я хотел реализовать именно эту карту в качестве очередного демо к проекту dbCartajs, но в Сети нашёл лишь копию карты, снятую на мобильный телефон с неважным качеством. Зато с легкостью нашел с десяток схем Московского метро. Самая красивая, на мой взгляд, в Википедии, самая неказистая оказалась почему-то у Яндекса с его-то возможностями. Собственно SVG-вариант из Википедии я и переделал под Canvas, о чем писал в предыдущей [статье](http://habrahabr.ru/post/193778).

Спустя некоторое время я нашел на форумах два варианта схем в формате JPEG и решил реализовать первоначальную задумку. Ссылки на источники я потерял, поэтому еще раз выложил эти картинки в оригинале, если кому интересно, здесь: [mosrailmap](http://img-fotki.yandex.ru/get/9307/136640652.0/0_d098d_385c6c23_orig) и [vkontur](http://img-fotki.yandex.ru/get/9312/136640652.0/0_d098e_42e80f72_orig).

Онлайн-версию моей версии карты можно увидеть на [dbcartajs.appspot.com](http://dbcartajs.appspot.com/mosrails.html). Из-за ограничений на количество просмотров на бесплатном хостинге сайт может быть заблокирован, поэтому я советую брать и смотреть проект с [github](https://github.com/egaxegax/dbCartajs).

Я постарался учесть комментарии пользователей к предыдущей схеме метро: шрифты и центрирование. В этой версии размер шрифта масштабируется по ширине карты, при центрировании выводится прицел на выбранную станцию из вертикальной и горизонтальной линий. Можно изучать схему расположения станций, узлов пересадок.

Для тех, кто впервые видит виджет dbCarta напомню про управление картой:

* Левый клик центрирует точку на карте в плоских проекциях, поворачивает глобус в сферических проекциях; 
* Кнопки масштаба [+|-] расположены на правой стороне карты.

Кроме того, навигация возможна по списку станций.

В общем, как говорится, жителям Подольска, Люберец и Луховиц добро пожаловать, москвичам просьба не беспокоить.<!--n:Сайт для блогов и карт/Схема пригородного движения жд сообщения Москвы и МО:s:83049:e:3765-->
<!----><!--2015-01-11 10:56:12-->
## Звездное небо на webGL с использованием three.js
В посте про ["Звездное небо на Canvas"](http://egaxegax.appspot.com/guestbook/532002) я уже описывал проект, где при помощи JavaScript на канвасе 2d формируется изображение глобуса Земли на фоне звезд, планет и орбит космических аппаратов. Для создания трехмерной картины звездного неба на плоскости я использовал формулы перевода трехмерных координат X, Y, Z отображаемых объектов: звезды, планеты, космические аппараты (КА), - в плоские декартовые координаты X, Y. Основную часть этих формул я взял из проекта [Marble](https://marble.kde.org/) для KDE. Портированный с C++ на JavaScript код я сохранил в файле **starry.js**.

![sky3d](https://img-fotki.yandex.ru/get/15512/136640652.1/0_1018c4_de8ac91d_orig.png)

Уже тогда я знал, что для вывода трехмерных объектов у канваса есть специальный движок webGL. Но для того, чтобы им воспользоваться нужно было близко познакомиться с этой технологией, а самое главное - найти качественные и понятные примеры его реализации. Те примеры, которые я смотрел, например, [khronos](https://www.khronos.org/registry/webgl/sdk/demos/webkit/Earth.html) с библиотеками J3DI0000.js и J3DIMath.js от Apple для работы с webGL, меня не вдохновляли: код громоздкий и сложный. Все изменилось, когда я познакомился с проектом [three.js](https://github.com/mrdoob/three.js). Простота написания кода и огромное количество примеров (работающих в оффлайне) в нем удивили и порадовали одновременно.

Уже почти закончив свою версию звездного неба в 3d, я познакомился с еще одним очень интересным проектом на [apoapys.com](http://apoapsys.com). Автор с помощью скриптов three.js воспроизводит объекты Солнечной Системы с эффектами, как в самой Celesia - эталонным для многих звездых проектов астрономическом атласе с открытым кодом. Из проекта apoapsys.com я позаимствовал координаты созвездий (файл **sfa_constellation_lines.js**), картинки для текстур звезд, облаков и космических аппаратов.

Свой код трехмерного неба, как и в плоской версии, я постарался сделать максимально простым и компактным, чтобы в нем легко можно было разобраться. Кроме того, я решил не использовать метод **window.requestAnimationFrame**, как в большинстве примеров из three.js и apoapsys.com, поскольку его использование сильно нагружает браузер и процессор. Для этого я использовал код из **OrbitControls.js** из three.js для управления камерой. Посмотреть трехмерную версию неба можно все там же на сайте проекта [dbcartajs](http://dbcartajs.appspot.com/sky3d.html).

## Что нового

В отличие от плоской версии неба здесь объекты Солнечной Системы показаны с учетом их реальных размеров и расстояний до них в км.

Для расчета орбит и положений КА используется код из **satellite.js**, как и в плоской версии. Данные о положении КА (TLE) обновлены с celestrak.com. В **tledata.js** добавил данные о группировках GLONASS, GPS, ISS (космические станции в т.ч. МКС).

## Управление

Управлять камерой можно мышью - поворот правой, смещение левой кнопкой и масштабирование колесиком, ма, стрелками на клавиатуре или через touch-интерфейс на сенсорных экранах. Собственно все события управления обрабатывает код из **OrbitControls.js**.

## Что еще

В планах научиться фокусировать в центре сцены другие объекты, кроме Земли, также добавить новые объекты - астероиды, кометы.<!--n:Сайт для блогов и карт/Звездное небо на webGL с использованием three.js:s:86977:e:5462-->
<!----><!--2023-02-23 12:40:09-->
## dbcartajs

Pan, zoom vector map and images (Canvas, SVG)<br>
*Просмотр векторных карт и изображений с навигацией в JavaScript*

Примеры ниже:

Интерактивные схемы метро Москвы со строящимися линиями и станциями и Петербурга в <i>2023</i> году, 
пригородного ж/д транспорта Москвы и МО в <i>2015</i> году.
По выбранным станциям рассчитывается кратчайший путь по алгоритму <i>BFS</i>.
Выбор станций возможен по клику, сброс маршрута - по двойному клику.

<table class="g scroll mw_f">
 <colgroup>
  <col width="300px">
  <col width="100px">
  <col width="100px">
  <col width="200px">
 </colgroup>
 <tr>
  <td width="320px" class=col> <i>Схема метро Москвы</i><br><sup>Moscow Metro</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/mosmetro.html"> Canvas </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/mosmetro.html"> SVG </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/mosmetro2.html"> SVG(Википедия) </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Схема ж/д Москвы и МО</i><br><sup>Moscow Railroad</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/mosrails.html"> Canvas </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/mosrails.html"> SVG </a> </td>
  <td></td>
 </tr>
 <tr>
  <td class=col> <i>Схема метро Петербурга</i><br><sup>St. Petersburg Metro</sup> </td>
  <td></td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/metrospb.html"> SVG </a> </td>
  <td></td>
 </tr>
 <tr>
  <td class=col> <i>Схема метро Тбилиси</i><br><sup>Tbilisi Metro</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/metro-tbilisi.html"> Canvas </a> </td>
  <td></td>
  <td></td>
 </tr>
</table>

Просмотр *jpeg* и *svg* картинок с возможностью масштабирования.

<table class="g scroll mw_f">
 <colgroup>
  <col width="300px">
  <col width="100px">
  <col width="100px">
 </colgroup>
 <tr>
  <td class=col width="320px"> <i>Просмотровщик картинок</i><br><sup>Image Viewer</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/imgviewer.html"> Canvas </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/imgviewer.html"> SVG </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Масштабирование картинки</i><br><sup>Pan Zoom</sup> </td>
  <td> - </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/panzoom.html"> SVG </a> </td>
 </tr>
</table>

Интерактивные карты мира со списками городов и стран в различных проекциях. 
Идея и стиль позаимствованы с примеров <a href="http://www.highcharts.com/maps/demo">highmaps</a> 

<table class="g scroll mw_f">
 <colgroup>
  <col width="300px">
  <col width="100px">
  <col width="100px">
 </colgroup>
 <tr>
  <td class=col width="320px"> <i>Атлас мира</i><br><sup>Atlas</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/atlas.html"> Canvas </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/atlas.html"> SVG </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Население мира</i><br><sup>Population</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/usemap.html"> Canvas </a> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/usemap.html"> SVG </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Население США</i><br><sup>Population USA</sup> </td>
  <td> - </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/us.html"> SVG </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Города мира</i><br><sup>Cities</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/cities.html"> Canvas </a> </td>
  <td> - </td>
 </tr>
 <tr>
  <td class=col> <i>Города России без расстояний</i><br><sup>Russian Cities</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/russ.html"> Canvas </a> </td>
  <td> - </td>
 </tr>
 <tr>
  <td class=col> <i>Страны мира</i><br><sup>Countries</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/countries.html"> Canvas </a> </td>
  <td> - </td>
 </tr>
 <tr>
  <td class=col> <i>Маршруты на карте</i><br><sup>Routes</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/merc.html"> Canvas </a> </td>
  <td> - </td>
 </tr>
</table>

Примеры использования градиента и *svg*-анимации с эффектом движения.

<table class="g scroll mw_f">
 <colgroup>
  <col width="300px">
  <col width="100px">
  <col width="100px">
 </colgroup>
 <tr>
  <td class=col width="320px"> <i>Настенные часы</i><br><sup>Wall Clock</sup> </td>
  <td> - </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/clock.html"> SVG </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Анимация движения</i><br><sup>Roller Ball</sup> </td>
  <td width="80px"> - </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/svg/rollerball.html"> SVG </a> </td>
 </tr>
</table>

Отрисовка картинки в канвасе <i>3d</i> с пересчетом проекции отображения через шейдеры <i>WebGL</i> на основе примеров с с сайта <a href="http://vcg.isti.cnr.it/~tarini/spinnableworldmaps/">Spinnable World Maps</a>. 
Звездное небо в канвасе <i>2d</i> и <i>3d</i> с использованием скриптов <a href="https://github.com/mrdoob/three.js">three.js</a>.

<table class="g scroll mw_f">
 <colgroup>
  <col width="300px">
  <col width="100px">
 </colgroup>
 <tr>
  <td class=col width="320px"> <i>Атлас 3D</i><br><sup>Atlas 3D</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/map3d.html"> Canvas </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Звездное небо</i><br><sup>Starry Sky</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/starry.html"> Canvas </a> </td>
 </tr>
 <tr>
  <td class=col> <i>Звездное небо 3D</i><br><sup>Sky 3D</sup> </td>
  <td> <a href="https://egaxegax.github.io/dbcartajs/sky3d.html"> Canvas </a> </td>
 </tr>
</table><!--n:Сайт для блогов и карт/Описание и примеры:s:92582:e:6588-->
<!----><!--2015-05-19 19:42:54-->
## Пересчет изображений под разные картографические проекции в webGL
В посте на своем блоге ["gdal_translate и gdalwarp для перепроицирования изображений"](http://egaxegax.appspot.com/guestbook/1122002) описывался процесс получения картинок под разные проекции с помощью утилит GDAL. Полученные изображения я использовал как подложку для карт в примерах проекта [dbCartajs](http://github.com/egaxegax/dbCartajs). Позже, работая над портированием канвасной версии своего планетария на webGL, описанной в статье ["Звездное небо на webGL с использованием three.js"](http://egaxegax.appspot.com/guestbook/4662364972515328) на Хабре, у меня возникла мысль со временем перенести не только глобус, но и плоские на карты на webGL, используя вместо фона текстуры.

![buttefly.png](https://img-fotki.yandex.ru/get/4209/136640652.1/0_112d01_d8377bc9_orig.png)

Мысль так и оставалась мыслью пока я не познакомился с очень интересным примером отображения картинки в разных проекциях на webGL ["Spinnable World Maps"](http://vcg.isti.cnr.it/~tarini/spinnableworldmaps/) от Марко Тарини. Этот пример показал коллега по работе еще год назад, но заинтересовался я им недавно. Код примера интересен еще и оригинальными комментариями автора на итальянском, например *punto centrale* или *mostra/nasconde griglia*.

Код Тарини оказался насыщен вычислениями всего чего угодно: размеров экрана, координат курсора мыши в пикселах и треугольниках, координат геометрий проекций, матриц поворота геометрий. При этом полностью картинка с меридианами и измененными цветами формируется в шейдерах. Мне захотелось отрисовать что-нибудь на этой карте, скажем границы стран. Но для этого пришлось бы вставлять код вычислений пикселов линий в код шейдера как с случае с меридианами, а это уже слишком. Поэтому возникла мысль совместить изображение карты в канвасе 2d с перепроицированием через webGL и формулы Тарини. То есть использовать канвас как источник текстуры для наложения на геометрию. В исходниках Three.js встречаются такие примеры.

Из кода Spinnable Maps я взял в основном вычислительные формулы, а из примеров dbcartajs - логику создания карты по слоям, пересчет координат мыши в пиксели, таймер. Результат слияния двух проектов можно посмотреть [здесь](http://dbcartajs.appspot.com/map3d.html).

Управлять картой можно мышью. При таскании мышью происходит вращение карты по сфере по 3 осям, а не смещение на плоскости. Это порождает эффект бесконечного зацикливания карты вдоль оси X.<!--n:Сайт для блогов и карт/Пересчет изображений под разные картографические проекции в webGL:s:99270:e:4116-->
<!----><!--2025-09-27 03:54:30-->Блог, посвященный разработке проекта [dbcartajs](https://github.com/egaxegax/dbcartajs).
Примеры и статьи доступны также в блоге на [dbcartajs.blogspot.ru](http://dbcartajs.blogspot.ru).<!--n:Сайт для блогов и карт/about:s:103570:e:286-->
<!----><!--2013-07-02 20:51:25-->
## Заметки, отзывы, планы проекта карты dbCartajs
Идея проекта создать инструмент отображения географических объектов (имеющих координаты), который можно было бы использовать на любых платформах для отладки и разработки более сложных геоинформационных систем.

Демо и исходники доступны на [dbcartajs.appspot.com](http://dbcartajs.appspot.com).

dbCartajs для рисования использует объект Canvas, который доступен в новых версиях браузеров, поддерживающих разметку HTML5.

Для пересчета координат из одной проекции в другую используется код [Proj4js](http://trac.osgeo.org/proj4js/). В версии 1.0 доступны следующие проекции:

* merc (Меркатор)
* ortho (Ортографическая)
* laea (Азимутальная проекция Ламберта)

Проекции пересчитываются из плоских декартовых координат longlat. Если скрипты Proj4js не подключены доступна только плоская проекция longlat.<!--n:Сайт для блогов и карт/Заметки, отзывы, планы проекта карты dbCartajs:s:103927:e:1453-->
<!----><!--2017-08-14 22:40:10-->
## Карты и Google Maps
Очень интересный сайт с тепловой картой цен на недвижимость Москвы и Санкт-Петербурга [https://квартиры-домики.рф/карта-цен](https://квартиры-домики.рф/%D0%BA%D0%B0%D1%80%D1%82%D0%B0-%D1%86%D0%B5%D0%BD)<!--n:Сайт для блогов и карт/Карты и Google Maps:s:105523:e:378-->
<!----><!--2015-10-15 21:38:36-->
## Карта Московского Метро. SVG-версия
Продолжаю тему разработки динамической векторной (по координатам) карты для браузера dbcartajs. В новой версии (v2) я перевел отрисовку объектов с канваса на SVG. И переделал несколько примеров, в частности карту метро Москвы. В своем посте про канвасную версию карты я сравнивал ее с svg-версией из Википедии, сделав акцент на скорости загрузки, которая у канваса оказалась выше. Но воспроизведя карту через svg-обработчик в новой версии проекта, я понял, что скорость загрузки, пожалуй, единственное преимущество канваса перед SVG.

![mosmetro-svg](https://habrastorage.org/getpro/habr/post_images/7a4/69c/883/7a469c883e9d6e9b8de63871ee68c1e5.jpg)

Во-первых, потребовалось меньшее количество кода для создания на svg.

Во-вторых, простота и удобство создания кода. У svg логика строится на отдельных объектах, их свойствах и методах. Например, чтобы определить объект под курсором, нужно создать обработчик события для данного объекта (circle для станций метро), в котором можно поменять его свойства — цвет, масштаб (на картинке для значка станции «Ходынское поле» применен метод scale) и др. У канваса логика отрисовки построена на перерисовке всей карты. И для выделения отдельных объектов нужно перерисовывать и масштабировать всю карту. Кроме этого, канвас не хранит отрисованные объекты в памяти, их нужно отдельно сохранять в переменных (в dbcartajs в объекте mflood) и самому следить за ними (добавлять, удалять). SVG-изображение хранит отрисованные объекты в DOM-модели и к ним можно обращаться напрямую.

В-третьих, возможностей в svg намного больше, чем в канвасе, например, анимация, фильтры для изображений.

В-четвертых, совместимость с браузерами. У SVG она выше. C SVG я проблем не заметил. В канвасе некоторые свойства в Firefox 3.x и новых версиях работают по разному (например setDashLine, isPointInPath). Internet Explorer до 9 версии и Safari до 4 версии канвас вообще не поддерживали.

И svg, и канвас могут манипулировать готовыми изображениями (png, jpeg). Правда, только канвас может обращаться к нему попиксельно. И это, как и скорость отрисовки, пожалуй, его главная особенность.

В общем, кому интересно, смотрите примеры на [dbcartajs.appspot.com](http://dbcartajs.appspot.com).<!--n:Сайт для блогов и карт/Карта Московского Метро. SVG-версия:s:105992:e:3836-->
<!----><!--2025-09-24 17:01:11-->
## Разработка статического сайта для блогов
Хочу предложить вниманию читателей свой проект разработки статического сайта
для публикации текстов и фотографий.  
  
Адрес сайта [egax.ru](https://egax.ru), зеркало [egaxegax.github.io](https://egaxegax.github.io).  
Репозиторий проекта [egaxegax.github.io](https://github.com/egaxegax/egaxegax.github.io).  
  
Я уже писал о нём на Хабре в другой [статье](https://habr.com/ru/articles/784388/), 
где в комментариях мне предложили использовать различные статические генераторы *Hugo*, *Jekyll*, *Eleventy*, *Netlify* и другие. В процессе изучения генераторов и языка *Nodejs*, который они используют, определенные наработки 
применил, например, парсер сайтов с аккордами *chords-parser* на *Nodejs*. Но мне хочется полной свободы в действиях, поэтому не хочу переходить на сторонние шаблонизаторы. Благо в прошлом я уже "наелся" программированием на *Python*-*Django-* и *Go*-шаблонах на *Google*-хостинге *appspot.com* . 
  
Я использую сайт для публикации своих заметок, скриптов, а также изучения возможностей языков *html5*, *javascript*, *svg*, *python*. Кроме этого я использую сайт как агрегатор статей, новостных сводок из RSS-лент с сайтов Дзен, Хабр, Спортс и других для чтения без навязчивой рекламы и лишней информации на самим порталах. Мне нравится программировать на *Python* и поэтому написал на нём скрипты чтения и парсинга RSS-лент, feed-листов в разделе *posts*:

* *readrss.py*    чтение новостей
* *readrufeed.py* чтение лент каналов рутуб
* *readsites.py*  чтение лент с разных сайтов
* *readyfeed.py*  чтение лент каналов ютуб
* *readylist.py*  чтение плейлиста ютуб
* *readzen.py*    чтение ленты дзен<!--n:Сайт для блогов и карт/Разработка статического сайта для блогов:s:109957:e:2678-->
<!----><!--2013-08-10 19:13:59-->
## Звездное небо на Canvas
В этой статье я хочу более подробно рассказать о примере [Starry Sky](http://dbcartajs.appspot.com/starry.html) (Звездное Небо), реализованном с помощью скриптов [dbCartajs](http://dbcartajs.appspot.com). Starry Sky включает в себя идеи других "звездных" проектов, которые были портированы на JavaScript. Рассмотрим их подробнее. Алгоритм формирования звездного неба был позаимствован из проекта Marble KDE (плагин stars), расчет положения планет построен на основе замечательной статьи шведского астронома [Поля Шлетера](http://stjarnhimlen.se/comp/ppcomp.html), модель движения космических аппаратов SGP4/SDP4 предоставлена модулем satellite-js (проект в github), формулы солнечного терминатора (ночной зоны) взяты с [астрономического форума](http://www.astronomy.ru/forum/index.php/topic,70976.msg1145154.html). Вид орбит как эллипсов подсмотрен у Сelestia.

Пример имеет чисто технологическое назначение: вывести в заданное время точку положения космического аппарата при заданных орбитальных параметрах. В Canvas это получилось очень красиво и я решил подробнее написать об этом. Если нужно что-то поменять в выводе объектов, настройках не нужно перекомпилировать программу как Marble или Xephem (и соответственно устанавливать компилятор или среду разработки) достаточно иметь лишь браузер. В Mozilla или Chrome уже есть встроенные панели отладки, где можно посмотреть, скажем, массив точек траектории аппарата. Это гораздо удобнее чем "вытаскивать" их из C-й.

## Управление

Вращение Земли происходит по клику в любой точке глобуса. В демо предусмотрен авторежим с ускорением времени (1 сек~15 минут, кнопка play рядом с датой). Анимацию с суточным периодом можно посмотреть [здесь](http://img-fotki.yandex.ru/get/9115/136640652.0/0_bf3ec_c1eb0a8_orig), простой скриншот приведен ниже.

![Starry Sky](http://img-fotki.yandex.ru/get/9555/136640652.0/0_becbd_66ad485b_XL.png)<!--n:Сайт для блогов и карт/Звездное небо на Canvas:s:112778:e:3109-->
