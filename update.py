#!/usr/bin/python3
#
# Update file list sorted descending by date from DIR to index.js.
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime,rootkey] = subject dir
#   TITLES = [subjkey,sortkey,name,lasttime,rootkey] = files in subj. dir
#
# python3 ../update.py ( run from dir vesti,foto,posts,songs,books)
#

import json, io, linecache, re, os, sys, time
from updatelist import main as updatelist_main, E_OS, tr

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]')
  return s

def hashstr(s):
  from ctypes import c_int32
  mhash = 0
  if s == '': return 0
  for t in list(s):
    mhash = (c_int32(mhash << 5).value - mhash) + ord(t)
    mhash |= 0
  return mhash

def main(path='.'):
  mfiles = []
  cwd = os.path.basename(os.path.abspath(path))
  sdir = cwd
  if sdir == 'posts':
    sdir = 'index'

  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:

      fname, ext = os.path.splitext(name)

      roots = E_OS(os.path.basename(os.path.dirname(root)))
      subj = E_OS(os.path.basename(root))
      title = E_OS(fname)

      if 'sitemap' in name or 'README' in name:
        print(os.path.join(root, name), '...skip')
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
          if not os.path.exists(os.path.join(root, 'th', fname+'.jpg')):
            im_th = ImageOps.exif_transpose(im)
            im_th.thumbnail((800,600))
            if not os.path.exists(os.path.join(root, 'th')):
              os.mkdir(os.path.join(root, 'th'))
            im_th.save(os.path.join(root, 'th', fname+'.jpg') , "JPEG")
      elif cwd in ('books', 'posts', 'songs') and ext in ('.md',):
        ftime = os.path.getmtime(os.path.join(root, name))
        if fname != 'about': # skip about
          line = linecache.getline(os.path.join(root, name), 1)
          if re.search(r'^\d+-\d+-\d+\s\d+:\d+:\d+', line[line.find('<!--')+4:][:19].strip('->')):
            ftime = time.mktime(time.strptime(line[line.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
          elif re.search(r'^\d{2}\d{2}\d{2} \d{2}\d{2}', name[:11]):
            ftime = time.mktime(time.strptime(name[:11], '%y%m%d %H%M'))
          else:
            raise ValueError(root, name, line)
      else:
        print(os.path.join(root, name), '...skip')
        continue
      mfiles.append([ roots, subj, title, int(time.strftime('%y%m%d%H%M%S', time.localtime(ftime))) ]) 

  mfiles.sort(key=lambda f: (f[3], f[1], f[2]), reverse=True)
  mroots = []
  msubj = []
  mtitles = []
  mcounter = 0
  murls = []

  surl = 'https://egax.ru'
  surl1 = 'https://egaxegax.github.io'

  for i, f in enumerate(mfiles):
    if f[2] == 'about':
      mcounter += 1
      continue
    iroot = -1
    for ii, root in enumerate(mroots):
      if f[0] == root[0]:
        root[1] += 1
        iroot = ii
        break
    if iroot == -1:
      mroots += [[f[0], 1, f[3]]]
      iroot = len(mroots) - 1
      murls += [[]]
    isubj = -1
    for ii, subj in enumerate(msubj):
      if f[1] == subj[0]:
        subj[1] += 1
        isubj = ii
        break
    if isubj == -1:
      msubj += [[f[1], 1, f[3], iroot]]
      isubj = len(msubj) - 1
      if len(murls) == 0:
        murls[iroot] += [surl +'/'+ sdir + '.html']
      murls[iroot] += [surl +'/'+ sdir + '.html?'+ tr(f[1])]
    mtitles += [[isubj, len(mfiles) - len(mtitles) - mcounter, f[2], f[3], iroot]]
    murls[iroot] += [surl +'/'+ sdir +'.html?'+ tr(f[1])+'/'+tr(f[2])]
    if sdir == 'foto':
      murls[iroot] += [surl +'/'+ sdir +'/'+ f[1] +'/'+ f[2]+ '.jpg']
    print( i )

  io.open(path + '/index.js', 'w', encoding='utf-8', newline='\n').write(compact('ROOTS=' + json.dumps(mroots, indent=0, ensure_ascii=0) + ';\n'))
  io.open(path + '/index.js', 'a', encoding='utf-8', newline='\n').write(compact('SUBJ=' + json.dumps(msubj, indent=0, ensure_ascii=0) + ';\n'))
  io.open(path + '/index.js', 'a', encoding='utf-8', newline='\n').write(compact('TITLES=' + json.dumps(mtitles, indent=0, ensure_ascii=0) + ';'))

  if murls:
    io.open(path + '/sitemap.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted([u for urls in murls for u in urls])))
    io.open(path + '/sitemap1.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted([u.replace(surl, surl1) for urls in murls for u in urls])))
    if cwd in ('songs', ): # split sitemap
      for i, u in enumerate(murls):
        io.open(path + '/sitemap_' +str('%02d' % i)+ '.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(u)))

  time.sleep(1)

if __name__ == '__main__':
  main()
  updatelist_main()