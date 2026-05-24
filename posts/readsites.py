#!python3
#
# Parse RSS .xml from sites to .md
#
# python3 readsites.py <RSSlist-id>
#

RSSlist = {
  'finecooking': {'hdr':'Подборка рецептов/finecooking.ru','url':'https://finecooking.ru/feed/rss',      'cut':480,                    'total':3, 'ctag': 'channel', 'itag': 'item', 'sm':'' },
  'habr':        {'hdr':'Подборка с сайтов/Хабр',          'url':'https://habr.com/ru/rss/news/?fl=ru',  'cut':480,                    'total':3, 'ctag': 'channel', 'itag': 'item', 'sm':''},
  'kino_kino':   {'hdr':'Подборка с сайтов/Кино-Театр.РУ', 'url':'https://kino-teatr.ru/rss/kino.xml',   'cut':1000,                   'total':2, 'ctag': 'channel', 'itag': 'item', 'sm':''},
  'kino_teatr':  {'hdr':'Подборка с сайтов/Кино-Театр.РУ', 'url':'https://kino-teatr.ru/rss/teatr.xml',  'cut':1000,                   'total':1, 'ctag': 'channel', 'itag': 'item', 'sm':''},
  'povarenok':   {'hdr':'Подборка рецептов/Поваренок.РУ',  'url':'https://www.povarenok.ru/rss/recipes/','cut':480,                    'total':3, 'ctag': 'channel', 'itag': 'item', 'sm':'' },
  'prosto_linux':{'hdr':'Подборка с сайтов/Prosto Linux',  'url':'https://prosto-linux.ru/feed',         'cut':1000,                   'total':10,'ctag': 'channel', 'itag': 'item', 'sm':''},
  'yaplakal':    {'hdr':'Подборка с сайтов/ЯПлакал',       'url':'https://www.yaplakal.com/news.xml',    'cut':2000,                   'total':7, 'ctag': 'channel', 'itag': 'item', 'sm':''},
  'flickr':      {'hdr':'Подборка с сайтов/Flickr.com',    'url':'http://api.flickr.com/services/feeds/photos_public.gne', 'cut':1000, 'total':10,'ctag': '',        'itag': 'entry','sm':'{http://www.w3.org/2005/Atom}'},
}

import os, sys, time, re
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import tr_chars, tr_cut
# from updaterssd import main as updaterss_main

fcount = 0

for id, prm in [[id, prm] for id, prm in RSSlist.items() if id in sys.argv]:
  with urlopen(Request(prm['url'], headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    rst = ET.fromstring(purl.read(), parser=ET.XMLParser())
    if prm.get('ctag'): rst = rst.find(prm['ctag'])
    for ii, item in [[ii, item] for ii, item in enumerate(rst.findall('%(sm)s%(itag)s' % prm)) if ii < prm['total']]:
      titl = item.find('%(sm)stitle' % prm).text.strip()
      if not titl:
        print('!!! No title tag. Skip...')
        continue
      link = item.find('%(sm)slink' % prm).text
      ptitl = ''
      if link: ptitl = '<p class="titl"><a href="{link}">{titl}</a></p>'.format(link=link, titl=titl)
      text = ''
      if item.find('description') is not None:         text = item.find('description').text.strip()
      if item.find('enclosure') is not None:           text = '<a href="{link}"><img src="{imurl}"></a>'.format(link=link, imurl=item.find('enclosure').get('url')) + text
      if item.find('%(sm)scontent' % prm) is not None: text = item.find('%(sm)scontent' % prm).text
      if not text or re.search('<!--Begin Video.*!--End Video-->', text):
        print('!!! No text tag. Skip...')
        continue
      pdate = ''
      if item.find('pubDate') is not None:               pdate = item.find('pubDate').text
      if item.find('%(sm)spublished' % prm) is not None: pdate = item.find('%(sm)spublished' % prm).text
      if not pdate:
        print('!!! No pdate tag. Skip...')
        continue
      if re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \+\w+$', pdate):
        pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %z')
      elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \w+$', pdate):
        pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %Z')
      elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \+\w+$', pdate):
        pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %z')
      elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \w+$', pdate):
        pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %Z')
      elif re.search(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\w+$', pdate):
        pdt = time.strptime(pdate, '%Y-%m-%dT%H:%M:%SZ')
      else:
        print('!!! pubDate %s is incorrect' % pdate)
        pdt = time.localtime()
      rdate = time.strftime('%Y-%m-%d', pdt)
      ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
      text = """{ctime}
<div class="yb">
  <div class="rss mw_f scroll {rssid}">{text} {titl}</div>
</div>
""".format(ctime=ctime, rssid=id, link=link, rdate=rdate, titl=ptitl, text=tr_chars(text, prm['cut']))
      if not os.path.exists(os.path.join(cdir, os.path.dirname(prm['hdr']))):
        os.mkdir(os.path.join(cdir, os.path.dirname(prm['hdr'])))
      if not os.path.exists(os.path.join(cdir, prm['hdr'])):
        os.mkdir(os.path.join(cdir, prm['hdr']))
      try:    open(os.path.join(cdir, prm['hdr'], tr_cut(titl) + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
      except: continue
      fcount += 1
  print(prm['hdr'], '(%s)' % (ii+1,))

if fcount:
  time.sleep(1)
  update_main(cdir)