#!/usr/bin/python3
#
# Update index.js from README
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime,rootkey] = subject dir
#   TITLES = [subjkey,[offset,len],name,lasttime,rootkey] = files in subj. dir
#
# python3 ../update.py (run from foto, posts, songs, books dirs)
#

import json, io, linecache, re, os, sys, time
from updatelist import tr

added = {}
skipped = {}

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n','\g<1>',s)
  s = s.replace('\n],[','],\n[').replace('[[','[\n[').replace('\n]]',']\n]').replace('\n],', '],')
  return s

def hashstr(s):
  from ctypes import c_int32
  mhash = 0
  if s == '': return 0
  for t in list(s):
    mhash = (c_int32(mhash << 5).value - mhash) + ord(t)
    mhash |= 0
  return mhash

def addimgtomd(impath, mdpath):
  if not os.path.exists(impath): return
  if not os.path.exists(mdpath): return
  from PIL import Image
  import base64
  buffer = io.BytesIO()
  im = Image.open(impath)
  im = im.convert('RGB')
  im.save(buffer, format='JPEG')
  cover = base64.b64encode(buffer.getvalue()).decode()
  cont = open(mdpath).read()
  tags = [tag for tag in re.split('(<!--[^<]*-->)', cont) if tag and tag.find('cover:') == -1]
  tags.insert(len(tags)-1, '<!--cover:'+ cover +'-->')
  # print(tags)
  open(mdpath, 'w').write(''.join(tags))
  os.remove(impath)

def addmdtoreadme(mdpath, ftime=''):
  name, ext = os.path.splitext(os.path.basename(mdpath))
  cont = open(mdpath).read()
  readme = os.path.join(os.path.dirname(mdpath), 'README')
  if os.path.exists(readme):
    with open(readme) as f:
      if '<!--n:'+ name +':' in f.read(): 
        print('Duplicate', name)
        os.remove(mdpath)
        return
  added[mdpath] = 1
  with open(readme, 'a') as f:
    of = f.tell()
    f.write('<!---->'+ ftime + cont.strip())
    f.write('<!--n:'+ name +':' +'s:'+ str(of) +':e:'+ str(f.tell() - of) +'-->\n')
    os.remove(mdpath)

def addimgtoreadme(impath, ftime=''):
  name, ext = os.path.splitext(os.path.basename(impath))
  readme = os.path.join(os.path.dirname(impath), 'README')
  if os.path.exists(readme):
    with open(readme) as f:
      if '<!--n:'+ name +':' in f.read(): 
        print('.', end='')
        return
  with open(readme, 'a') as f:
    of = f.tell()
    f.write('<!---->'+ ftime)
    f.write('<!--n:'+ name +':' +'s:'+ str(of) +':e:'+ str(f.tell() - of) +'-->\n')

def readmetoindex(roots, subj, readmepath):
  mlist = []
  with open(readmepath) as f:
    for item in [item for item in re.split('<!---->', f.read()) if item]:
      try:
        ftime = time.mktime(time.strptime(item[item.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
        ftime = int(time.strftime('%y%m%d%H%M%S', time.localtime(ftime)))
      except:
        print(f, item)
        raise
      m = re.search(r'<!--n:([^:]+):s:(\d+):e:(\d+)-->', item)
      if m: 
        mlist += [[roots, subj, m[1], ftime, [int(m[2]), int(m[3])]]]
  return mlist

def addskipped(name):
  ext = os.path.splitext(name)[-1] or name
  if not ext in skipped: skipped[ext] = 0
  skipped[ext] += 1

def main(path='.'):
  cwd = os.path.basename(os.path.abspath(path))

  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
      fname, ext = os.path.splitext(name)
      roots = os.path.basename(os.path.dirname(root))
      subj = os.path.basename(root)

      if root == path:
        continue

      if 'sitemap' in name or 'README' in name:
        addskipped(name)
        continue

      if cwd in ('books',) and name in ('about.md',): addimgtomd(os.path.join(root, 'about.jpg'), os.path.join(root, name))
      if cwd in ('books',) and ext in ('.jpg',):      addimgtomd(os.path.join(root, name), os.path.join(root, fname+'.md'))
      if cwd in ('songs',) and ext in ('.jpg',):      addimgtomd(os.path.join(root, name), os.path.join(root, 'about.md'))
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
      
      if cwd in ('foto',) and ext.lower() in ('.jpg',):
        ftime = os.path.getmtime(os.path.join(root, name))
        if subj == 'th': # skip preview
          addskipped(subj)
          continue
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
              print('err', root, name)
              raise
          if not os.path.exists(os.path.join(root, 'th', fname+'.jpg')): # thumbnails
            im_th = ImageOps.exif_transpose(im)
            im_th.thumbnail((800,600))
            if not os.path.exists(os.path.join(root, 'th')):
              os.mkdir(os.path.join(root, 'th'))
            im_th.save(os.path.join(root, 'th', fname+'.jpg') , "JPEG")
        ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime)) +'-->'
        addimgtoreadme(os.path.join(root, name), ftime)
      elif cwd in ('books', 'posts', 'songs', 'foto') and ext in ('.md',):
        line = linecache.getline(os.path.join(root, name), 1)
        ftime = ''
        if re.search(r'^\d+-\d+-\d+\s\d+:\d+:\d+', line[line.find('<!--')+4:][:19].strip('->')):
          pass
        elif re.search(r'^\d{2}\d{2}\d{2} \d{2}\d{2}', name[:11]):
          ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(name[:11], '%y%m%d %H%M')) +'-->'
        else:
          ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(root, name)))) +'-->'
        addmdtoreadme(os.path.join(root, name), ftime)
      else:
        addskipped(name)
        continue

  mfiles = []
  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
      roots = os.path.basename(os.path.dirname(root))
      subj = os.path.basename(root)

      if root == path:
        continue

      if 'README' in name and cwd in ('books', 'posts', 'songs', 'foto'):
        mfiles += readmetoindex(roots, subj, os.path.join(root, name))
      else:
        continue

  mfiles.sort(key=lambda f: (f[3], f[1], f[2]), reverse=True)
  mroots = []
  msubj = []
  mtitles = []
  murls = []

  surl = 'https://egax.ru'
  surl1 = 'https://egaxegax.github.io'
  sdir = cwd
  if sdir == 'posts':
    sdir = 'index'

  for i, f in enumerate(mfiles):
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
    mtitles += [[isubj, f[4], f[2], f[3], iroot]]
    murls[iroot] += [surl +'/'+ sdir +'.html?'+ tr(f[1])+'/'+tr(f[2])]
    if sdir == 'foto':
      murls[iroot] += [surl +'/'+ sdir +'/'+ f[1] +'/'+ f[2]+ '.jpg']
  print( '\n===', cwd, '===\nUpdated:', len(mfiles), '\nAdded:', len(added), '\nSkipped:', tuple(k+':'+str(v) for k,v in skipped.items()) )

  mroots_s = sorted(mroots)
  msubj_s = sorted(msubj)
  mtitles = [[msubj_s.index(msubj[titl[0]]), titl[1], titl[2], titl[3], mroots_s.index(mroots[titl[4]])] for ii, titl in enumerate(mtitles)]
  msubj_s = [[subj[0], subj[1], subj[2], mroots_s.index(mroots[subj[3]])] for subj in msubj_s]

  io.open(path + '/index.js', 'w', encoding='utf-8', newline='\n').write(compact('ROOTS=' + json.dumps(mroots_s, indent=0, ensure_ascii=0) + ';\n'))
  io.open(path + '/index.js', 'a', encoding='utf-8', newline='\n').write(compact('SUBJ=' + json.dumps(msubj_s, indent=0, ensure_ascii=0) + ';\n'))
  io.open(path + '/index.js', 'a', encoding='utf-8', newline='\n').write(compact('TITLES=' + json.dumps(mtitles, indent=0, ensure_ascii=0) + ';'))

  if murls:
    io.open(path + '/sitemap.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted([u for urls in murls for u in urls])))
    io.open(path + '/sitemap1.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted([u.replace(surl, surl1) for urls in murls for u in urls])))
    if cwd in ('songs', ): # split sitemap
      for i, u in enumerate(murls):
        io.open(path + '/sitemap_' +str('%02d' % i)+ '.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(u)))

  time.sleep(1)

if __name__ == '__main__':
  main(*sys.argv[1:])