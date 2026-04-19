#!python3
#
# Convert .fb2 to .md and .jpg files.
#
# python books2fb2.py <fb2_dir> [<out_dir>]
#

import sys, os, re, time
import io, base64
from PIL import Image
from bs4 import BeautifulSoup

cd = os.path.dirname(sys.argv[0])
sys.path.insert(0, os.path.abspath(os.path.join(cd, '..')))

from update import main as update_main
from updatelist import tr_cut, tr_chars

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

GENRES_RU = {
  'Детективы': ['det', 'detective', 'foreign_detective', 'thriller'],
  'Детская литература': ['child', 'foreign_children'],
  'Документальная литература': ['nonf', 'nonfiction'],
  'Домоводство':['home'],
  'Драматургия':['dramaturgy', 'literature'],
  'Искусство и Дизайн':[''],
  'Любовные романы':['love'],
  'Наука и Образование':['sci', 'science', 'science_history'],
  'Приключения':['adv', 'adventure', 'foreign_adventure'],
  'Проза':['prose', 'foreign_prose', 'foreign_contemporary', 'russian_contemporary', 'lyrics', 'poetry'],
  'Проза. Классика': ['prose_classic'],
  'Проза. Политика':['literature_political'],
  'Психология':['sci_psychology', 'sci_philosophy'],
  'Религия и Эзотерика':['religion'],
  'Спорт':['home_sport'],
  'Справочная литература':['ref','reference'],
  'Старинная литература':['antique'],
  'Фантастика':['sf', 'foreign_sf'],
  'Фантастика. Ужасы':['sf_horror'],
  'Фэнтези':['sf_fantasy', 'magician_book', 'fantasy_fight', 'foreign_fantasy', 'adventure_fantasy', 'fantasy_rus', 'fantasy_heroic', 'historical_fantasy'],
  'Фэнтези. Попаданцы':['popadancy', 'popadanec'],
  'Экономика и Финансы':['economics'],
  'Эротика и Секс':['love_erotica', 'home_sex'],
  'Юмор':['humor']
}

if __name__ == '__main__':
  path = '.'
  bookdir = '.'
  if (len(sys.argv) > 1): path = os.path.abspath(E_OS(sys.argv[1]))
  if (len(sys.argv) > 2): bookdir = os.path.abspath(E_OS(sys.argv[2]))

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
        gnrs = fb.get_tags()

        if gnrs: subj = gnrs[0].split('/')[0].split(',')[0].replace('-', '_').replace(':', '').strip()
        else:    subj = 'other'

        for gnr_ru, gnrs in GENRES_RU.items():
          if subj in gnrs:               subj = gnr_ru
          if subj.split('_')[0] in gnrs: subj = gnr_ru

        pdate = fb.get_pubdate().split('-')[0]
        desc = fb.get_description()
        desc = desc.replace('&lt;','<').replace('&gt;','>')
        desc = re.sub('<[^<]+?>', '', desc).strip()
        cover = fb.get_cover_image()

        fp = os.path.join(bookdir, subj, re.sub('\s+', ' ', wrt))

        ftime = os.path.getmtime(os.path.join(root, name))
        sdate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ftime))

        if fp:
          j += 1
          try:    os.makedirs(fp, exist_ok=True)
          except: print('Err name:', fp) ; continue 
          if cover:
            try:
              im = Image.open(io.BytesIO(base64.b64decode(cover)))
              im = im.convert('RGB')
              im.thumbnail((240,240))
              buffer = io.BytesIO()
              im.save(buffer, format='JPEG')
              cover = base64.b64encode(buffer.getvalue()).decode()
            except:
              print (fb2name, ':', str(sys.exc_info()))
          with open(os.path.join(fp, tr_cut(tr_chars(tit[:160], 150, ''))+'.md'), 'w+') as fbook:
            fbook.write('<!--'+sdate+'--><!--pdate:'+pdate+'--><!--cover:'+cover+'--><!--gnr:'+','.join(gnrs).replace(':', '').replace('-','_').strip()+'-->\n' + desc)
          print (i, j, int(cover != None), fb2name)
        else:
          print(i, j, fb2name, '!!!SKIP:', 'desc:', tit, 'cover:', cover)

  input("Press to continue indexing...")
  update_main(os.path.dirname(__file__))
