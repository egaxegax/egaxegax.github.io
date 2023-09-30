<!--2012-11-20 20:10:44-->
### Python Расширенный аналог утилиты wc в Linux
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
```