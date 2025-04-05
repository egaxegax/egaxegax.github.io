#!python3
#
# Parse RSS .xml page to .md
#
# python3 readrss.py <RSSlist-id>
#

RSSlist = {
  'anekdot_day': {'hdr':'Анекдоты из России', 'url':'https://www.anekdot.ru/rss/export20.xml'},
  'anekdot_10': {'hdr':'Анекдоты из России', 'url':'https://www.anekdot.ru/rss/export_j.xml'},
}

import os, sys, time, re, locale
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import main as updatelist_main, tr_chars
from updateturbo import main as updateturbo_main

def parsePubDate(item):
  pdate = item.find('pubDate').text
  if re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2}:\d{2} \+\w+$', pdate):
    return time.strptime(pdate, '%a, %d %b %Y %H:%M:%S %z')
  elif re.search(r'^\w+, \d+ \w+ \d{4} \d{2}:\d{2} \+\w+$', pdate):
    return time.strptime(pdate, '%a, %d %b %Y %H:%M %z')
  else:
    print('pubDate %s is incorrect!!!' % pdate)
    return time.localtime()

total = 10
fcount = 0
for ri, (id, prm) in enumerate([(id, prm) for id, prm in RSSlist.items() if id in sys.argv]):
  with urlopen(Request(prm['url'], headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for channel in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('channel'):
      cdtm = parsePubDate(channel)
      if not os.path.exists(os.path.join(cdir, str(cdtm.tm_year))):
        os.mkdir(os.path.join(cdir, str(cdtm.tm_year)))
      with open(os.path.join(cdir, str(cdtm.tm_year), '{y}{m}{d} {h}{c}.md'.format(y=time.strftime('%y', cdtm), m=('%02d' % cdtm.tm_mon), d=('%02d' % cdtm.tm_mday), h=('%02d' % cdtm.tm_hour), c=('%02d' % ri))), 'w+', encoding='utf-8', newline='\n') as fp:
        locale.setlocale(locale.LC_ALL, 'Russian')
        fp.write('<h3>'+prm['hdr']+' на '+ time.strftime('%a %d %b %Y %H:%M', cdtm) +'</h3>')
        locale.setlocale(locale.LC_ALL, 'C')
        for ii, item in [[ii, item] for ii, item in enumerate(channel.findall('item')) if ii < total]:
          link = item.find('link').text
          titl = item.find('description').text
          ptitl = titl+' <a class="nodecor" href="{link}">&lt;...&gt;</a>'.format(link=link, titl=tr_chars(titl, 255))
          pdate = parsePubDate(item)
          text = """
<div class="rssn table">
  {titl}
</div><p></p>""".format(titl=ptitl)
          fp.write(text)
          fcount += 1
      print(prm['hdr'], prm['url'], '(%s)' % (ii,))

if fcount:
  time.sleep(1)
  os.chdir(cdir)
  update_main()
  updatelist_main()
  updateturbo_main()