#!python3
#
# Parse RSS .xml page to .md and run index.py
#

RSSlist = {
  'Подборка IT-новостей от Хабра': {'url': 'https://habr.com/ru/rss/news/?fl=ru', 'titl':'title'},
  'EADaily Европейские новости': {'url': 'https://eadaily.com/ru/rss/index.xml', 'titl':'title'},
  # 'РИА Новости': {'url': 'https://ria.ru/export/rss2/index.xml', 'titl':'title'},
  'Кино-Театр.РУ Мир театра': {'url': 'https://kino-teatr.ru/rss/teatr.xml', 'titl':'description'},
  'Кино-Театр.РУ Новости кино': {'url': 'https://kino-teatr.ru/rss/kino.xml', 'titl':'description'}
}

import os, sys, time, datetime, dateutil.parser
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)

sys.path.insert(0, cdir+'/..')
from update import main as update_main
from updatelist import main as updatelist_main, tr_chars

import locale

fcount = 0
rcount = 0

for hdr, prm in RSSlist.items():
  icount = 0
  rcount += 1
  with urlopen(Request(prm['url'], headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for channel in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall("channel"):
      cdtm = time.localtime()
      if not os.path.exists(os.path.join(cdir, str(cdtm.tm_year))):
        os.mkdir(os.path.join(cdir, str(cdtm.tm_year)))
      with open(os.path.join(cdir, str(cdtm.tm_year), '{y}{m}{d} {h}{c}.md'.format(y=time.strftime('%y', cdtm), m=('%02d' % cdtm.tm_mon), d=('%02d' % cdtm.tm_mday), h=('%02d' % cdtm.tm_hour), c=('%02d' % rcount))), 'w+', encoding='utf-8', newline='\n') as fp:
        locale.setlocale(locale.LC_ALL, 'Russian')
        fp.write('<h3>'+hdr+' на '+ time.strftime('%c', cdtm) +'</h3>')
        locale.setlocale(locale.LC_ALL, 'C')
        for item in channel.findall('item'):
          if icount >= 20:
            break
          ptitl = item.find(prm['titl']).text
          if prm['titl'] == 'title':
            ptitl = tr_chars(ptitl, 70)
          phref = item.find('link').text
          pdate = item.find('pubDate').text
          pdt = dateutil.parser.parse(pdate)
          text = """
<div class="rss table">
  <span class="smaller gray hspace">{ph}:{pmi}</span>
  <a class="nodecor" href="{phref}">{titl}</a>
</div>""".format(titl=ptitl, phref=phref, ph=('%02d' % pdt.time().hour), pmi=('%02d' % pdt.time().minute))
          fp.write(text)
          fcount += 1
          icount += 1
      print(hdr, prm['url'], '(%s)' % (icount,))

if fcount:
  time.sleep(1)
  os.chdir(cdir)
  update_main()
  updatelist_main()
  