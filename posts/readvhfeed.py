#!python3
#
# Parse VoyeurHit sitemap list to .md
#

RSSlist = [
  ('Подборка из VoyeurHit/Spy Cam, Upskirt', 'sitemap_vids_70'),
  # https://voyeurspycam.live/rss.xml
]

import os, sys, time
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)
sys.path.insert(0, cdir+'/..')

from update import main as update_main
from updatelist import main as updatelist_main, tr, tr_chars, tr_cut
from updaterssd import main as updaterss_main

fcount = 0

for hdr, url in RSSlist:
  feedurl =  'http://voyeurhit.tube/'+url
  with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for ii, item in [[ii, item] for ii, item in enumerate(ET.fromstring(purl.read(), parser=ET.XMLParser())[-1000:])]:
      item_video = item.find('{http://www.google.com/schemas/sitemap-video/1.1}video')
      titl = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}title').text
      udate = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}publication_date').text
      videoid = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}player_loc').text
      desc = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}description').text
      cat = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}category').text
      imurl = item_video.find('{http://www.google.com/schemas/sitemap-video/1.1}thumbnail_loc').text
      mtitl = tr_cut(titl)
      if not mtitl: 
        print(titl, '...Skip')
        continue
      phref = '/index.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
      pdt = time.strptime(udate, '%Y-%m-%dT%H:%M:%S%z')
      rdate = time.strftime('%Y-%m-%d', pdt)
      ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
#       # print('\n', '\n'.join([mtitl, phref, rdate, imurl, authr, videoid]))
      text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    <img class="preview" data-adult="1" data-videoid="{videoid}" src="{imurl}" align="left" alt="">
  </a>
  <div class="inlbl text">
    <p><a class="nodecor" href="{phref}">{titl}</a></p>
    <p><i class="smaller2">{cat}</i></p>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, imurl=imurl, rdate=rdate, videoid=videoid, titl=tr_chars(titl, 200), cat=cat)
      if not os.path.exists(os.path.join(cdir, hdr)):
        os.makedirs(os.path.join(cdir, hdr))
      open(os.path.join(cdir, hdr, mtitl + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
      fcount += 1
    print(hdr, url, '(%s)' % (fcount,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  updateturbo_main(cdir)