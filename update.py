#!/usr/bin/python3
#
# Update file list sorted descending by date from DIR to index.js.
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime,rootkey] = subject dir
#   TITLES = [subjkey,sortkey,name,lasttime,rootkey] = files in subj. dir
#
# python3 ../update.py ( run from dir vesti,posts,songs,books)
#

import json
import linecache
import re
import os
import sys
import time
import io

def E_OS(text):
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

    if cwd in ('songs',) and ext in ('.txt',):
      text = open(os.path.join(root, name), encoding='utf-8', newline='\n').read()
      text = re.sub('[\t ]*\n', '\n', text)
      text = re.sub('(^|\n)!([\t ]*)(.*)', r'\1\2*\3*', text)
      text = re.sub('(^|\n)>([\t ]*)(.*)', r'\1\2***\3***', text)
      text = re.sub('<([\t ]*)([^!>]*)([\t ]*)>', r'\1***\2***\3', text)
      text = re.sub('^[\r\n]+|[\r\n]+$', '', text)
      text = re.sub('\r', '', text)
      text = re.sub('\t', ' ', text)
      text = re.sub(' ', r' ', text)  # unicode space (html not trim)
      text = re.sub('\n', '  \n', text) # two spaces newline
      text = re.sub('(^<\!--.*-->)\n[\t ]*\n*', r'\1\n', text) # revert comments
      open(os.path.join(root, fname + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
      os.remove(os.path.join(root, name))
      name = fname + '.md'
      ext = '.md'

    if cwd in ('vesti',) and ext in ('.md',):
      if fname != 'about': # skip about
        ftime = time.mktime(time.strptime(name[:11], '%y%m%d %H%M'))
    elif cwd in ('foto',) and ext.lower() in ('.jpg',):
      ftime = os.path.getmtime(os.path.join(root, name))
      if subj == 'th': 
        continue  # skip preview
      else:
        from PIL import Image, ImageOps
        from PIL.ExifTags import TAGS
        import locale
        im = Image.open(os.path.join(root, name))
        exifs = im._getexif()
        if exifs and exifs.get(306):    # DateTime exists
          ftime = time.mktime(time.strptime(exifs.get(306), '%Y:%m:%d %H:%M:%S'))
        else:
          try:
            sdate = name.split('.')
            sdate = sdate[len(sdate) - 2].strip().split(' ')
            sdate = sdate[0][:3] + ' ' + sdate[1]
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
            ftime = time.mktime(time.strptime(sdate, '%b %Yг'))
          except:
            print(root, name)
            raise
        # make thumbnails
        im_th = ImageOps.exif_transpose(im)
        im_th.thumbnail((800,600))
        if not os.path.exists(os.path.join(root, 'th')):
          os.mkdir(os.path.join(root, 'th'))
        im_th.save(os.path.join(root, 'th', fname+'.jpg') , "JPEG")
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
    if len(murls) == 0:
      murls += [surl +'/'+ sdir + '.html']
    murls += [surl +'/'+ sdir + '.html?'+ TR(f[1])]
  mtitles += [[isubj, len(mfiles) - len(mtitles) - abcounter, f[2], f[3], iroots]]
  murls += [surl +'/'+ sdir +'.html?'+ TR(f[1]+'/'+f[2])]
  if sdir == 'foto':
    murls += [surl +'/'+ sdir +'/'+ f[1] +'/'+ f[2]+ '.jpg']
  print( i )

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]')
  return s

io.open('index.js', 'w', encoding='utf-8', newline='\n').write(compact('ROOTS=' + json.dumps(mroots, indent=0, ensure_ascii=0) + ';\n'))
io.open('index.js', 'a', encoding='utf-8', newline='\n').write(compact('SUBJ=' + json.dumps(msubj, indent=0, ensure_ascii=0) + ';\n'))
io.open('index.js', 'a', encoding='utf-8', newline='\n').write(compact('TITLES=' + json.dumps(mtitles, indent=0, ensure_ascii=0) + ';'))
if murls:
  io.open('sitemap.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(murls))
time.sleep(1)

sitemap = open('../sitemap.txt', 'w', newline='\n') # truncate file
sitemap = open('../sitemap.txt', 'a', newline='\n')

for d in ['books', 'foto', 'posts', 'songs', 'vesti', 'dbcartajs']:
  try:
    sitemap.write(open('../' + d + '/sitemap.txt').read() + '\n')
    print(d + ' added to sitemap.txt',)
  except: 
    print(d + ' skip')

import updatelist
