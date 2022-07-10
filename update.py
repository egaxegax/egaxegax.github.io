#!/usr/bin/python
#
# Update file list sorted descending by date from DIR to index.js.
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime,rootkey] = subject dir
#   TITLES = [subjkey,sortkey,name,lasttime,rootkey] = files in subj. dir
#
# python ../update.py ( run from dir vesti,posts,songs,books)
#

import json
import linecache
import re
import os
import sys
import time

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
  return text

def TR(t):
  ru = {
    'а':'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 
    'е':'e', 'ё':'e', 'ж':'j', 'з':'z', 'и':'i', 'й':'j', 
    'к':'k', 'л':'l', 'м':'m', 'н':'n', 'о':'o', 
    'п':'p', 'р':'r', 'с':'s', 'т':'t', 'у':'u', 
    'ф':'f', 'х':'h', 'ц':'c', 'ч':'ch', 'ш':'sh', 
    'щ':'shch', 'ы':'y', 'э':'e', 'ю':'ju', 'я':'ya'
  }
  tr = []
  t = re.sub(r'[ъь\'"`\(\)%]+','',t)
  t = re.sub(r'[\s\.,]+','_',t)
  for s in t:
    tr.append( ru.get( s ) or ru.get( s.lower(), s ) )
  return ''.join(tr).lower()

path = '.'
mfiles = []

surl = 'https://egaxegax.github.io'
sdir = os.path.basename(os.getcwd())
if sdir == 'vesti':
  sdir = 'index'

for root, dirs, files in os.walk(path, topdown=False):
  for name in files:

    fname, ext = os.path.splitext(name)

    roots = E_OS(os.path.basename(os.path.dirname(root)))
    subj = E_OS(os.path.basename(root))
    title = E_OS(fname)
    cwd = os.path.basename(os.getcwd())

    if name in ('README.md', 'sitemap.txt'):
      continue

    if cwd in ('vesti',) and ext in ('.md',):
      if fname != 'about': # skip about
        ftime = time.mktime(time.strptime(name[:11], '%y%m%d %H%M'))
    elif cwd in ('foto',) and ext.lower() in ('.jpg',):
      from PIL import Image
      ftime = os.path.getmtime(os.path.join(root, name))
      im = Image.open(os.path.join(root, name))
      im.thumbnail((100,100))
      if not os.path.exists(os.path.join(root, 'th')):
        os.mkdir(os.path.join(root, 'th'))
      im.save(os.path.join(root, 'th', fname+'.jpeg') , "JPEG")
    elif cwd in ('books', 'posts', 'songs') and ext in ('.md',):
      ftime = os.path.getmtime(os.path.join(root, name))
      if fname != 'about': # skip about
        line = linecache.getline(os.path.join(root, name), 1)
        try: 
          ftime = time.mktime(time.strptime(line[line.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
        except:
          print(root, name,)
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
murls = []

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
    msubj += [[f[1], 1, f[3], iroots]]
    isubj = len(msubj) - 1
    murls += [surl +'/'+ sdir + ('.html?'+ TR(f[1]), '/'+ f[1])[sdir == 'foto']]
  mtitles += [[isubj, len(mfiles) - len(mtitles) - abcounter, f[2], f[3], iroots]]
  murls += [surl +'/'+ sdir +('.html?'+ TR(f[1]+'/'+f[2]), '/'+ f[1] +'/'+ f[2]+ '.JPG')[sdir == 'foto']]
  print( i )

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]')
  return s

open('index.js', 'w').write(compact('ROOTS=' + json.dumps(mroots, indent=0, ensure_ascii=0) + ';\n'))
open('index.js', 'a').write(compact('SUBJ=' + json.dumps(msubj, indent=0, ensure_ascii=0) + ';\n'))
open('index.js', 'a').write(compact('TITLES=' + json.dumps(mtitles, indent=0, ensure_ascii=0) + ';'))
if murls:
  open('sitemap.txt', 'w').write('\n'.join(murls))
time.sleep(1)

sitemap = open('../sitemap.txt', 'w') # truncate file
sitemap = open('../sitemap.txt', 'a')

for d in ['books', 'posts', 'songs', 'vesti', 'dbcartajs']:
  try:
    sitemap.write(open('../' + d + '/sitemap.txt').read() + '\n')
    print(d + ' added to sitemap.txt',)
  except: 
    print(d + ' skip')

import updatelist