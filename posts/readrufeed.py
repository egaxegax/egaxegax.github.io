#!python3
#
# Parse RuTube author_id videos list .xml to .md
#
# text from: https://darkrutube.tumblr.com/api_video
#

RSSList = [
  ('Подборка из Rutube/Политика(США)', '23550697'),
]

import os, sys, time
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import main as updatelist_main, tr, tr_chars, tr_cut
from updateturbo import main as updateturbo_main

fcount = 0

for hdr, url in RSSlist:
  feedurl =  'http://rutube.ru/api/video/person/'+url
  with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for ii, item in [[ii, item] for ii, item in enumerate(ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('{http://www.w3.org/2005/Atom}entry')) if ii < 10]:
      titl = item.find('{http://www.w3.org/2005/Atom}title').text
      udate = item.find('{http://www.w3.org/2005/Atom}published').text
      videoid = item.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
      authr = item.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
      imurl= item.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}thumbnail').get('url')
      mtitl = tr_cut(titl)
      phref = '/index.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
      pdt = time.strptime(udate, '%Y-%m-%dT%H:%M:%S%z')
      rdate = time.strftime('%Y-%m-%d', pdt)
      ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
      # print('\n', '\n'.join([mtitl, phref, rdate, imurl, authr, videoid]))
      text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    <img class="preview" data-videoid="{videoid}" src="{imurl}" align="middle" alt="">
  </a>
  <div class="inlbl text">
    <a class="nodecor" href="{phref}">{titl}</a><br>
    <i class="smaller2">{authr}</i><br>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, imurl=imurl, rdate=rdate, videoid=videoid, titl=tr_chars(titl, 60), authr=authr)
      if not os.path.exists(os.path.join(cdir, hdr)):
        os.mkdir(os.path.join(cdir, hdr))
      open(os.path.join(cdir, hdr, mtitl + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
      fcount += 1
    print(hdr, url, '(%s)' % (ii+1,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  updateturbo_main(cdir)