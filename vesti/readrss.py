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

fcount = 0

import urllib.request

with urllib.request.urlopen("https://habr.com/ru/rss/articles/?fl=ru") as purl:
  rsstext = purl.read().decode("utf8")
  if rsstext:
    root = ET.fromstring(rsstext)
    for channel in root.findall("channel"):
      gdate = channel.find('pubDate').text
      gdt = time.strptime(gdate, "%a, %d %b %Y %H:%M:%S %Z")
      if not os.path.exists(os.path.join(cdir, str(gdt.tm_year))):
        os.mkdir(os.path.join(cdir, str(gdt.tm_year)))
      with open(os.path.join(cdir, str(gdt.tm_year), '{y}{m}{d} 0300.md'.format(y=time.strftime('%y', gdt), m=('%02d' % gdt.tm_mon), d=('%02d' % gdt.tm_mday))), 'w+', encoding='utf-8', newline='\n') as fp:
        fp.write("<h3>Свежая подборка статей с Хабра</h3>")
        for item in channel.findall("item"):
          titl = item.find('title').text
          phref = item.find('link').text
          pdate = item.find('pubDate').text
          pdt = time.strptime(pdate, "%a, %d %b %Y %H:%M:%S %Z")
          text = """
<div class="rss">
  <span class="smaller gray hspace">{ph}:{pmi}</span>
  <a class="nodecor" href="{phref}">{titl}</a>
</div>""".format(titl=tr_chars(titl, 70), phref=phref, ph=('%02d' % pdt.tm_hour), pmi=('%02d' % pdt.tm_min))
          print(gdate, text)
          fp.write(text)
          fcount += 1

if fcount:
  os.chdir(cdir)
  update_main()
  updatelist_main()
  