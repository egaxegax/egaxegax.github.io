#!/usr/bin/python3
#
# Update index.js from README
#
#   ROOTS  = [name,count,lasttime] = root dir
#   SUBJ   = [name,count,lasttime,rootkey] = subject dir
#   TITLES = [subjkey,[offset,len],name,lasttime,rootkey] = files in subj. dir
#
# python3 update.py {foto, posts, songs, books}
#

import json, io, linecache, re, os, sys, time
from updatelist import tr

added = {}
skipped = {}
mdcache = {}

def compact(s):
  s = re.sub(r'([\[,\]]+)\s*\n',r'\g<1>',s)
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
  cont = open(mdpath, encoding='utf-8', newline='\n').read()
  tags = [tag for tag in re.split('(<!--[^<]*-->)', cont) if tag and tag.find('cover:') == -1]
  tags.insert(len(tags)-1, '<!--cover:'+ cover +'-->')
  # print(tags)
  open(mdpath, 'w', encoding='utf-8', newline='\n').write(''.join(tags))
  os.remove(impath)

def addmdtoreadme(mdpath, ftime='', islastfile=0):
  name, ext = os.path.splitext(os.path.basename(mdpath))
  cont = open(mdpath, encoding='utf-8', newline='\n').read()
  readme = os.path.join(os.path.dirname(mdpath), '..', 'README.md')
  rskey = os.path.basename(os.path.dirname(os.path.dirname(mdpath)))
  skip = 0
  if not rskey in mdcache:
    if os.path.exists(readme): mdcache[rskey] = open(readme, encoding='utf-8', newline='\n').read()
    else:                      mdcache[rskey] = ''
  if '<!--n:'+ os.path.basename(os.path.dirname(mdpath)) +'/'+ name +':' in mdcache[rskey]:
    print('.', end='')
    os.remove(mdpath)
    addskipped('Duplicate')
    skip = 1
  if not skip:
    with open(readme, 'a', encoding='utf-8', newline='\n') as f:
      of = f.tell()
      f.write('<!---->'+ ftime + cont.strip())
      f.write('<!--n:'+ os.path.basename(os.path.dirname(mdpath)) +'/'+ name +':' +'s:'+ str(of) +':e:'+ str(f.tell() - of) +'-->\n')
      os.remove(mdpath)
      added[mdpath] = 1
  if islastfile:
    try:    os.rmdir(os.path.dirname(mdpath))
    except: pass

def addimgtoreadme(impath, ftime=''):
  name, ext = os.path.splitext(os.path.basename(impath))
  readme = os.path.join(os.path.dirname(impath), '..', 'README.md')
  added[impath] = 1
  with open(readme, 'a', encoding='utf-8', newline='\n') as f:
    of = f.tell()
    f.write('<!---->'+ ftime)
    f.write('<!--n:'+ os.path.basename(os.path.dirname(impath)) +'/'+ name +':' +'s:'+ str(of) +':e:'+ str(f.tell() - of) +'-->\n')
  if os.path.exists(os.path.splitext(impath)[0] + '.md'):
    os.remove(os.path.splitext(impath)[0] + '.md')

def readmetoindex(readmepath):
  mlist = []
  with open(readmepath, encoding='utf-8', newline='\n') as f:
    for item in [item for item in re.split('<!---->', f.read()) if item]:
      try:
        ftime = time.mktime(time.strptime(item[item.find('<!--')+4:][:19].strip('->'), '%Y-%m-%d %H:%M:%S'))
        ftime = int(time.strftime('%y%m%d%H%M%S', time.localtime(ftime)))
      except:
        print(f, item)
        raise
      m = re.search(r'<!--n:([^:]+):s:(\d+):e:(\d+)-->', item)
      try:    subj, titl = m[1].split('/')
      except: print('Err ', item); continue
      mlist += [[os.path.basename(os.path.dirname(readmepath)), subj, titl, ftime, [int(m[2]), int(m[3])]]]
  return mlist

def addskipped(name):
  ext = os.path.splitext(name)[-1] or name
  if not ext in skipped: skipped[ext] = 0
  skipped[ext] += 1

def main(path='.'):
  cwd = os.path.basename(os.path.abspath(path))

  for root, dirs, files in os.walk(path, topdown=False):
    for ifile, name in enumerate(files):
      fname, ext = os.path.splitext(name)
      subj = os.path.basename(root)

      if root == path:
        continue

      if 'sitemap' in name or 'README' in name:
        addskipped(fname)
        continue

      if cwd in ('books',) and name in ('about.md',): addimgtomd(os.path.join(root, 'about.jpg'), os.path.join(root, name))
      if cwd in ('books',) and ext in ('.jpg',):      addimgtomd(os.path.join(root, name), os.path.join(root, fname+'.md'))
      if cwd in ('songs',) and ext in ('.jpg',):      addimgtomd(os.path.join(root, name), os.path.join(root, 'about.md'))
      if cwd in ('songs',) and ext in ('.txt',):
        text = open(os.path.join(root, name), encoding='utf-8', newline='\n').read()
        text = re.sub(r'[\t ]*\n', '\n', text)
        text = re.sub(r'(^|\n)!([\t ]*)(.*)', r'\1\2*\3*', text)
        text = re.sub(r'(^|\n)>([\t ]*)(.*)', r'\1\2***\3***', text)
        text = re.sub(r'<([\t ]*)([^!>]*)([\t ]*)>', r'\1***\2***\3', text)
        text = re.sub(r'^[\r\n]+|[\r\n]+$', '', text)
        text = re.sub(r'\r', '', text)
        text = re.sub(r'\t', ' ', text)
        text = re.sub(r' ', r' ', text)  # unicode space (html not trim)
        text = re.sub(r'\n', '  \n', text) # two spaces newline
        text = re.sub(r'(^<\!--.*-->)\n[\t ]*\n*', r'\1\n', text) # revert comments
        open(os.path.join(root, fname + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
        os.remove(os.path.join(root, name))
        name = fname + '.md'
        ext = '.md'
      
      if cwd in ('foto',) and ext.lower() in ('.jpg',):
        ftime = os.path.getmtime(os.path.join(root, name))
        if subj == 'th': # skip preview
          addskipped(subj)
          continue
        try:
          from PIL import Image, ImageOps
          from PIL.ExifTags import TAGS
          im = Image.open(os.path.join(root, name))
          exifs = im._getexif()
          if exifs and exifs.get(306):    # DateTime exists
            ftime = time.mktime(time.strptime(exifs.get(306), '%Y:%m:%d %H:%M:%S'))
          if not os.path.exists(os.path.join(root, 'th', fname+'.jpg')): # thumbnails
            im_th = ImageOps.exif_transpose(im)
            im_th.thumbnail((800,600))
            if not os.path.exists(os.path.join(root, 'th')):
              os.mkdir(os.path.join(root, 'th'))
            im_th.save(os.path.join(root, 'th', fname+'.jpg') , "JPEG")
        except:
          print(*sys.exc_info())
        ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime)) +'-->'
        addimgtoreadme(os.path.join(root, name), ftime)
      elif cwd in ('books', 'posts', 'songs') and ext in ('.md',):
        line = linecache.getline(os.path.join(root, name), 1)
        ftime = ''
        if re.search(r'^\d+-\d+-\d+\s\d+:\d+:\d+', line[line.find('<!--')+4:][:19].strip('->')):
          pass
        elif re.search(r'^\d{2}\d{2}\d{2} \d{2}\d{2}', name[:11]):
          ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(name[:11], '%y%m%d %H%M')) +'-->'
        else:
          ftime = '<!--'+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(os.path.join(root, name)))) +'-->'
        addmdtoreadme(os.path.join(root, name), ftime, ifile == len(files) - 1)
      else:
        addskipped(name)
        continue

  mfiles = []
  for root, dirs, files in os.walk(path, topdown=False):
    for name in files:
      if root == path:
        continue

      if 'README' in name and cwd in ('books', 'posts', 'songs', 'foto'):
        mfiles += readmetoindex(os.path.join(root, name))
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
  print( '\n', cwd, ': Updated:', len(mfiles), 'Added:', len(added), 'Skipped:', tuple(k+':'+str(v) for k,v in skipped.items()) )

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
    # if cwd in ('songs', ): # split sitemap
    #   for i, u in enumerate(murls):
    #     io.open(path + '/sitemap_' +str('%02d' % i)+ '.txt', 'w', encoding='utf-8', newline='\n').write('\n'.join(sorted(u)))

  time.sleep(1)

if __name__ == '__main__':
  main(*sys.argv[1:])