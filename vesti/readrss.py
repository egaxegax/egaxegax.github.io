#!python3
#
# Parse and index RSS xml to .md and index.js files
#

import os, sys, time
import xml.etree.ElementTree as ET
import urllib.request

cdir = os.path.dirname(__file__)

sys.path.insert(0, cdir+'/..')
from update import main as update_main
from updatelist import main as updatelist_main, tr_chars

import locale

RSSlist = {
  'Подборка статей с Хабра': 'https://habr.com/ru/rss/articles/?fl=ru',
  'РИА Новости' :'https://ria.ru/export/rss2/index.xml'
}
fcount = 0
rcount = 0

for hdr, url in RSSlist.items():
  rcount += 1
  with urllib.request.urlopen(url) as purl:
    rsstext = purl.read().decode("utf8")
    if rsstext:
      root = ET.fromstring(rsstext)
      for channel in root.findall("channel"):
        cdtm = time.localtime()
        if not os.path.exists(os.path.join(cdir, str(cdtm.tm_year))):
          os.mkdir(os.path.join(cdir, str(cdtm.tm_year)))
        with open(os.path.join(cdir, str(cdtm.tm_year), '{y}{m}{d} {h}{c}.md'.format(y=time.strftime('%y', cdtm), m=('%02d' % cdtm.tm_mon), d=('%02d' % cdtm.tm_mday), h=('%02d' % cdtm.tm_hour), c=('%02d' % rcount))), 'w+', encoding='utf-8', newline='\n') as fp:
          locale.setlocale(locale.LC_ALL, 'Russian')
          fp.write('<h3>'+hdr+' на '+ time.strftime('%c', cdtm) +'</h3>')
          locale.setlocale(locale.LC_ALL, 'C')
          for item in channel.findall('item'):
            if fcount/rcount >= 20:
              break
            titl = item.find('title').text
            phref = item.find('link').text
            pdate = item.find('pubDate').text
            print(pdate)
            pdt = time.strptime(pdate.replace('+0300','MSK'), '%a, %d %b %Y %H:%M:%S %Z')
            text = """
<div class="rss">
  <span class="smaller gray hspace">{ph}:{pmi}</span>
  <a class="nodecor" href="{phref}">{titl}</a>
</div>""".format(titl=tr_chars(titl, 70), phref=phref, ph=('%02d' % pdt.tm_hour), pmi=('%02d' % pdt.tm_min))
            print(cdtm, text)
            fp.write(text)
            fcount += 1

if fcount:
  os.chdir(cdir)
  update_main()
  updatelist_main()
  