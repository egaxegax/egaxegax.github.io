#!python3
#
# Parse RSS .xml from sites to .md
#
# python3 readsites.py <RSSlist-id>
#

RSSlist = {
  'habr': {'hdr':'Подборка с сайтов/Хабр', 'url':'https://habr.com/ru/rss/news/?fl=ru', 'cut':480, 'total':10},
  'kino_kino': {'hdr':'Подборка с сайтов/Кино-Театр.РУ', 'url':'https://kino-teatr.ru/rss/kino.xml', 'cut':1000, 'total':5},
  'kino_teatr': {'hdr':'Подборка с сайтов/Кино-Театр.РУ', 'url':'https://kino-teatr.ru/rss/teatr.xml', 'cut':1000, 'total':5},
  # 'povar': {'hdr':'Подборка рецептов/Повар.РУ', 'url':'https://povar.ru/rss', 'cut':480, 'total':5},
  'povarenok': {'hdr':'Подборка рецептов/Поваренок.РУ', 'url':'https://www.povarenok.ru/rss/recipes/', 'cut':480, 'total':5},
  'finecooking': {'hdr':'Подборка рецептов/finecooking.ru', 'url':'https://finecooking.ru/feed/rss', 'cut':480, 'total':7},
}

import os, sys, time, re
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import main as updatelist_main, tr_chars, tr_cut
from updateturbo import main as updateturbo_main

fcount = 0

for id, prm in [[id, prm] for id, prm in RSSlist.items() if id in sys.argv]:
  with urlopen(Request(prm['url'], headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for channel in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('channel'):
      for ii, item in [[ii, item] for ii, item in enumerate(channel.findall('item')) if ii < prm['total']]:
        titl = item.find('title').text
        link = item.find('link').text
        text = item.find('description').text
        if not text: continue
        for encl in item.findall('enclosure'):
          text = '<a href="{link}"><img src="{imurl}"></a>'.format(link=link, imurl=encl.get('url')) + text
        ptitl = '<p class="titl"><a href="{link}">{titl}</a></p>'.format(link=link, titl=titl)
        pdate = item.find('pubDate').text
        if re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \+\w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %z')
        elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %Z')
        elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \+\w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %z')
        elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %Z')
        else:
          print('pubDate %s is incorrect!!!' % pdate)
          pdt = time.localtime()
        rdate = time.strftime('%Y-%m-%d', pdt)
        ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
        text = """{ctime}
<div class="yb">
  <div class="rss {rssid}">{text} {titl}</div>
</div>
""".format(ctime=ctime, rssid=id, link=link, rdate=rdate, titl=ptitl, text=tr_chars(text, prm['cut']))
        if not os.path.exists(os.path.join(cdir, os.path.dirname(prm['hdr']))):
          os.mkdir(os.path.join(cdir, os.path.dirname(prm['hdr'])))
        if not os.path.exists(os.path.join(cdir, prm['hdr'])):
          os.mkdir(os.path.join(cdir, prm['hdr']))
        try:    open(os.path.join(cdir, prm['hdr'], tr_cut(titl) + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
        except: continue
        fcount += 1
  print(prm['hdr'], '(%s)' % (ii,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  updateturbo_main(cdir)