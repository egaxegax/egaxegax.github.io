<!--2023-09-30 23:23:09-->
### Python Ресурсивное объединение файлов в каталогах
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
```