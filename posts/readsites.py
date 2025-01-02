#!python3
#
# Parse RSS .xml from sites to .md
#
# python3 readsites.py <RSSlist-id>
#

RSSlist = {
  'Подборка с сайтов/Хабр': {'id':'habr', 'url':'https://habr.com/ru/rss/news/?fl=ru'},
  'Подборка с сайтов/Кино-Театр': {'id':'kino_kino', 'url':'https://kino-teatr.ru/rss/kino.xml'},
  'Подборка с сайтов/Кино-Театр.РУ': {'id':'kino_teatr', 'url':'https://kino-teatr.ru/rss/teatr.xml'},
}

import os, sys, time, re
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import main as updatelist_main, tr_chars, tr_cut

total = 21
fcount = 0
cdtm = time.localtime()

for hdr, prm in [[hdr, prm] for hdr, prm in RSSlist.items() if prm['id'] in sys.argv]:
  with urlopen(Request(prm['url'], headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for channel in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall("channel"):
      for ii, item in [[ii, item] for ii, item in enumerate(channel.findall('item')) if ii < total]:
        titl = item.find('title').text
        link = item.find('link').text
        text = item.find('description').text
        ptitl = '<a class="light" href="{link}">{titl}</a>'.format(link=link, titl=titl)
        pdate = item.find('pubDate').text
        pdate = pdate.replace('+0300','MSK').replace('+0400','MSK')
        if re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %Z')
        elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \w+$', pdate):
          pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %Z')
        else:
          print('pubDate %s is incorrect!!!' % pdate)
          pdt = time.localtime()
        rdate = time.strftime('%Y-%m-%d', pdt)
        ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
        text = """{ctime}
<div class="yb">
  <div class="rss smaller1">{text} <br><br>{titl}</div>
</div>
""".format(ctime=ctime, link=link, rdate=rdate, titl=ptitl, text=tr_chars(text, 380))
        if not os.path.exists(os.path.join(cdir, os.path.dirname(hdr))):
          os.mkdir(os.path.join(cdir, os.path.dirname(hdr)))
        if not os.path.exists(os.path.join(cdir, hdr)):
          os.mkdir(os.path.join(cdir, hdr))
        open(os.path.join(cdir, hdr, tr_cut(titl) + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
        fcount += 1
  print(hdr, '(%s)' % (ii,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  