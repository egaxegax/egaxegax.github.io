#!python3
#
# Extract .epub to .txt and .jpg files.
#
# books2.py <dir_with_epub>

import sys, os, re, time
import zlib, zipfile, io
from PIL import Image

def E_OS(text):
  if os.name == 'nt':
    return text.decode('cp1251').encode('utf-8')
  return text

path = '.'
if (len(sys.argv) > 1):
  path = os.path.abspath(E_OS(sys.argv[1]))

i = 0
j = 0

for root, dirs, files in os.walk(path, topdown=False):
  for name in files:
    epubname = os.path.normpath(os.path.join(root, name))
    fname, ext = os.path.splitext(epubname)
    if (ext == '.epub'):
      i += 1

      if not zipfile.is_zipfile(epubname):
        print (name, ' not a valid ZIP')
        continue

      za = zipfile.ZipFile(epubname)
      filelist = za.namelist()
      filelist.sort()

      desc = ''
      cover = ''
      for f in filelist:
        if (f == 'content.opf'):
          ftext = za.read(f).decode('utf-8')
          tit = re.findall('>([^><]*)</dc:title>', ftext)[0]
          writer = re.findall('>([^><]*)</dc:creator>', ftext)[0]
          subj = re.findall('>([^><]*)</dc:subject>', ftext) 
          try:    desc = re.findall('<dc:description>(.*)</dc:description>', ftext, re.M | re.S)[0]
          except: desc = ''
          desc = desc.replace('&lt;','<').replace('&gt;','>')
          desc = re.sub('<[^<]+?>', '', desc).strip()
          if subj: subj = subj[0]
          else:    subj = 'other'

          fp = os.path.join('out', subj.strip(), re.sub('\s+', ' ', writer.strip()))
          for s in '<>:"/\|?*':
            tit = tit.strip().replace(s,'')
          ftime = os.path.getmtime(os.path.join(root, name))
          sdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

        if (f.find('cover')>-1 and (f.find('.jpg')>-1 or f.find('.jpe')>-1 or f.find('.png')>-1)):
          cover = f

      if desc and cover:
        j += 1
        if not os.path.exists(fp):
          os.makedirs(fp)
        fbook = open(os.path.join(fp, tit+'.md'), 'w+')
        fbook.write('<!--' + sdate + '-->\n' + desc)
        fbook.close()
        try:
          im = Image.open(io.BytesIO(za.read(cover)))
          im.thumbnail((240,240))
          im.save(os.path.join(fp, tit+'.jpg') , "JPEG")
        except:
          print (epubname, 'Not an valid image')
          raise
        print (i, j, epubname)
