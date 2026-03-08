#!python3
#
# Parse VoyeurSpycam.live rss to .md
#

RSSlist = [
  ('Подборка из VoyeurSpycam/Скрытая камера', 'https://voyeurspycam.live/rss.xml'),
]

import os, sys, time, re
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import tr, tr_chars, tr_cut
# from updaterssd import main as updaterss_main

fcount = 0

for hdr, url in RSSlist:
  feedurl =  url
  with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for channel in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('channel'):
      for ii, item in [[ii, item] for ii, item in enumerate(channel.findall('item')) if ii < 20]:
        titl = item.find('title').text
        pdate = item.find('pubDate').text
        link = item.find('link').text
        imurl = item.find('description').text
        cat = item.find('category').text
        mtitl = tr_cut(titl)
        if not mtitl: 
          print(titl, '...Skip')
          continue
        phref = '/index.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
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
  #       # print('\n', '\n'.join([mtitl, phref, rdate, imurl, authr, videoid]))
        text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    {imurl}
  </a>
  <div class="inlbl text">
    <p><a class="nodecor" href="{phref}">{titl}</a></p>
    <p><i class="smaller2">{cat}</i></p>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, imurl=imurl, rdate=rdate, titl=tr_chars(titl, 200), cat=cat)
        if not os.path.exists(os.path.join(cdir, hdr)):
          os.makedirs(os.path.join(cdir, hdr))
        open(os.path.join(cdir, hdr, mtitl + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
        fcount += 1
      print(hdr, url, '(%s)' % (fcount,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  # updaterss_main(cdir, chadult='adult')