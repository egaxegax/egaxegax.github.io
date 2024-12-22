#!python3
#
# Parse RSS .xml page to .md and run index.py
#

RSSlist = {
  'EADaily Европейские новости': {'id':'eadaily', 'url': 'https://eadaily.com/ru/rss/index.xml', 'titl':'title'},
  'Подборка IT-новостей от Хабра': {'id':'habr', 'url': 'https://habr.com/ru/rss/news/?fl=ru', 'titl':'title'},
  'РИА Новости': {'id': 'ria', 'url': 'https://ria.ru/export/rss2/index.xml', 'titl':'title'},
  'Кино-Театр.РУ Мир театра': {'id':'kino_teatr', 'url': 'https://kino-teatr.ru/rss/teatr.xml', 'titl':'description'},
  'Кино-Театр.РУ Новости кино': {'id':'kino_kino', 'url': 'https://kino-teatr.ru/rss/kino.xml', 'titl':'description'}
}

import os, sys, time, re
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
  if prm['id'] in sys.argv:
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
            if icount < 20:
              phref = item.find('link').text
              ptitl = item.find(prm['titl']).text or item.find('title').text
              if prm['titl'] == 'title': ptitl = '<a class="nodecor" href="{phref}">{titl}</a>'.format(phref=phref, titl=tr_chars(ptitl, 70))
              pdate = item.find('pubDate').text
              pdate = pdate.replace('+0300','MSK').replace('+0400','MSK')
              if re.search(r'^\w+, \d{2} \w+ \d{4} \d{2}:\d{2}:\d{2} \w+$', pdate):
                pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %Z')
              elif re.search(r'^\w+, \d{2} \w+ \d{4} \d{2}:\d{2} \w+$', pdate):
                pdt = time.strptime(pdate, '%a, %d %b %Y %H:%M %Z')
              else:
                print('pubDate %s is incorrect!!!' % pdate)
                pdt = cdtm
              text = """
<div class="rss table">
  <span class="smaller gray hspace">{ph}:{pmi}</span>
  {titl}
</div>""".format(titl=ptitl, ph=('%02d' % pdt.tm_hour), pmi=('%02d' % pdt.tm_min))
              fp.write(text)
              fcount += 1
              icount += 1
        print(hdr, prm['url'], '(%s)' % (icount,))

if fcount:
  time.sleep(1)
  os.chdir(cdir)
  update_main()
  updatelist_main()
  