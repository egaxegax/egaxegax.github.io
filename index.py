#!/usr/bin/python
#
# List sorted files from PATH to index.js with COMMIT git commt+push action if passed.
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime] = subject dir
#   TITLES = [subjkey,sortkey,name,lasttime,rootkey] = files in subj. dir
#
# python index.py PATH COMMIT
#
#   PATH = news|posts|songs|books
#   COMMIT = [0|1] git commit+push (optional)
#

import json
import linecache
import re
import os
import sys
import time
from PIL import Image

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
  return text

path = '.'
mfiles = []
gitskip = 1

if len(sys.argv) > 1:
  gitskip = (sys.argv[1] != "1")

for root, dirs, files in os.walk(path, topdown=False):
  for name in files:

    fname, ext = os.path.splitext(name)

    roots = E_OS(os.path.basename(os.path.dirname(root)))
    subj = E_OS(os.path.basename(root))
    title = E_OS(fname)
    cwd = os.path.basename(os.getcwd())

    if cwd in ('news') and ext in ('.txt'):
      ftime = time.mktime(time.strptime(name[:11], '%y%m%d %H%M'))
    elif cwd in ('fotki') and ext.lower() in ('.jpg'):
      title = E_OS(name)
      ftime = os.path.getmtime(os.path.join(root, name))
      im = Image.open(os.path.join(root, name))
      im.thumbnail((100,100))
      if not os.path.exists(os.path.join(root, 'th')):
        os.mkdir(os.path.join(root, 'th'))
      im.save(os.path.join(root, 'th', fname+'.jpeg') , "JPEG")
    elif cwd in ('books','posts','songs') and ext in ('.txt'):
      ftime = os.path.getmtime(os.path.join(root, name))
      if fname != 'about':
        line = linecache.getline(os.path.join(root, name), 1)
        try: 
          ftime = time.mktime(time.strptime(line[line.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
        except:
          raise
    else:
      print(name, '...skip')
      continue

    mfiles.append([ roots, subj, title, int(time.strftime('%y%m%d%H%M%S', time.localtime(ftime))) ]) 

mfiles.sort(key=lambda f: f[3], reverse=True)
mroots = []
msubj = []
mtitles = []
abcounter = 0

for i, f in enumerate(mfiles):
  if f[2] == 'about':
    abcounter += 1
    continue
  iroots = -1
  for ii, roots in enumerate(mroots):
    if f[0] == roots[0]:
      roots[1] += 1
      iroots = ii
      break
  if iroots == -1:
    mroots += [[f[0], 1, f[3]]]
    iroots = len(mroots) - 1
  isubj = -1
  for ii, subj in enumerate(msubj):
    if f[1] == subj[0]:
      subj[1] += 1
      isubj = ii
      break
  if isubj == -1:
    msubj += [[f[1], 1, f[3]]]
    isubj = len(msubj) - 1
  mtitles += [[isubj, len(mfiles) - len(mtitles) - abcounter, f[2], f[3], iroots]]
  print( i )

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]')
  return s

open('index.js', 'w').write(compact('ROOTS=' + json.dumps(mroots, indent=0, ensure_ascii=0) + ';\n'))
open('index.js', 'a').write(compact('SUBJ=' + json.dumps(msubj, indent=0, ensure_ascii=0) + ';\n'))
open('index.js', 'a').write(compact('TITLES=' + json.dumps(mtitles, indent=0, ensure_ascii=0) + ';'))
time.sleep(1)

try:
  import subprocess
  if os.name == 'nt':
    os.putenv('PATH', '"c:/program files/git/bin"')
  if gitskip == 0: gitskip = subprocess.call('git add *.txt *.js *.html', shell=True)
  comment = '++' + os.path.basename(os.getcwd())
#  if gitskip == 0: raw_input(comment + ' Continue commit and push to github.com?')
  if gitskip == 0: gitskip = subprocess.call('git config --global user.email egax@ya.ru', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config --global user.name  egax', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git config core.fileMode false', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git commit -m "' + comment + '"', shell=True)
  if gitskip == 0: gitskip = subprocess.call('git push origin master', shell=True)
except:
  raise
