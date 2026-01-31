#!python3
#
# Covvert .fb2 to .md and .jpg files.
#
# python books2fb2.py <fb2_dir>
#

import sys, os, re, time
import io, base64
from PIL import Image
from bs4 import BeautifulSoup

cd = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.abspath(cd + '../'))

from update import main as update_main
from updatelist import main as updatelist_main, tr_chars

class fb2book:
  def __init__(self, file):
    self.file = file
    self.fb2_content = ''
    for e in ('utf-8', 'windows-1251'):
      if self.fb2_content == '':
        try:
          with open(file, 'r+', encoding=e) as fb2file:
            self.fb2_content = fb2file.read().encode(e)
            self.encoding = e
        except: pass
    if self.fb2_content == '': 
      raise ValueError('fb2_content encoding')
    self.soup = BeautifulSoup(self.fb2_content, "xml", from_encoding=self.encoding)
    self.info = self.soup.find('title-info') if self.soup.find('title-info') else None

  def get_pubdate(self):
    return self.info.find('date').text if self.info.find('date') else ''

  def get_title(self):
    return self.info.find('book-title').text if self.info.find('book-title') else ''

  def get_authors(self):
    authors = []
    for author in self.info.find_all('author'):
        a = []
        a += [author.find('first-name').text if author.find('first-name') else '']
        a += [author.find('last-name').text if author.find('last-name') else '']
        a += [author.find('middle-name').text if author.find('middle-name') else '']
        a += [author.find('nickname').text if author.find('nickname') else '']
        authors += [' '.join(a).strip()]
    return ', '.join([a for a in authors[:3] if a])

  def get_description(self):
    return self.info.find('annotation').text if self.info.find('annotation') else '' or \
           tr_chars(self.soup.find('body').text[:800], 780) if self.soup.find('body') else ''

  def get_tags(self):
    return [genre.text for genre in self.info.find_all('genre') if genre.text]

  def get_cover_image(self):
    return self.soup.find('binary', {'content-type': 'image/jpeg'}).text if self.soup.find('binary', {'content-type': 'image/jpeg'}) else '' or \
           self.soup.find('binary', {'content-type': 'image/jpg'}).text if self.soup.find('binary', {'content-type': 'image/jpg'}) else '' or \
           self.soup.find('binary', {'content-type': 'image/png'}).text if self.soup.find('binary', {'content-type': 'image/png'}) else ''

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
    fb2name = os.path.normpath(os.path.join(root, name))
    fname, ext = os.path.splitext(fb2name)
    if (ext == '.fb2'):
      i += 1

      fp = ''
      desc = ''
      cover = ''

      try: fb = fb2book(fb2name)
      except: raise ValueError(name)
    
      tit = fb.get_title()
      tit = tit.replace('[', '(').replace(']', ')').replace('/', '-').replace(':', '.').strip('<>"/\|!?*').strip()
      wrt = fb.get_authors()
      if not wrt:
        print(name, '!!!SKIP:', 'author not defined')
        continue
      wrt = wrt.replace('[', '(').replace(']', ')').replace('/', '-').strip(' <>:"/\|!?*')
      subj = fb.get_tags()

      if subj: subj = subj[0].split('/')[0].split(',')[0].replace('-', '_').strip()
      else:    subj = 'other'
      pdate = fb.get_pubdate().split('-')[0]
      desc = fb.get_description()
      desc = desc.replace('&lt;','<').replace('&gt;','>')
      desc = re.sub('<[^<]+?>', '', desc).strip()
      cover = fb.get_cover_image()

      fp = os.path.join('.', subj.replace(':', '').strip(), re.sub('\s+', ' ', wrt))
      
      ftime = os.path.getmtime(os.path.join(root, name))
      sdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

      if fp:
        j += 1
        os.makedirs(fp, exist_ok=True)
        if cover:
          try:
            im = Image.open(io.BytesIO(base64.b64decode(cover)))
            im.thumbnail((240,240))
            buffer = io.BytesIO()
            im.save(buffer, format='JPEG')
            cover = base64.b64encode(buffer.getvalue()).decode()
          except:
            print (fb2name, ':', str(sys.exc_info()))
        with open(os.path.join(fp, tr_chars(tit[:60], 50, '')+'.md'), 'w+') as fbook:
          fbook.write('<!--'+sdate+'--><!--pdate:'+pdate+'--><!--cover:'+cover+'-->\n' + desc)
        print (i, j, int(cover != None), fb2name)
      else:
        print(i, j, fb2name, '!!!SKIP:', 'desc:', tit, 'cover:', cover)

input("Press to continue indexing...")
update_main(os.path.dirname(__file__))
updatelist_main(os.path.dirname(__file__))