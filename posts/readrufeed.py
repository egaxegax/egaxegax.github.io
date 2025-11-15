#!python3
#
# Parse RuTube author_id videos list .xml to .md
#
# api from: https://darkrutube.tumblr.com/api_video
#

RSSlist = [
  ('Подборка из Rutube/Жизнь в США и России', '23550697'),#Саня во Флориде
  ('Подборка из Rutube/Мир кино', '1397853'),#GreenGrass
  ('Подборка из Rutube/Мир кино', '26313118'),#TVHub
  ('Подборка из Rutube/Рок-музыка', '24297472'),#Спи с Дилли
  ('Подборка из Rutube/Тайны', '31604927'),#Свидетель Windows
  ('Подборка из Rutube/Тайны', '23871528'),#ДИГГЕР ДАНИИЛ ДАВЫДОВ
  # ('Подборка из Rutube/Советские фильмы', '1792500'),
  # ('Подборка из Rutube/Сериалы', '33999143'),
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
  feedurl =  'http://rutube.ru/api/video/person/'+url+'?format=xml'
  with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for ii, item in [[ii, item] for ii, item in enumerate(ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('results/list-item')) if ii < 100]:
      titl = item.find('title').text
      udate = item.find('last_update_ts').text
      videoid = item.find('video_url').text
      authr = item.find('author/name').text
      imurl= item.find('thumbnail_url').text
      mtitl = tr_cut(titl)
      phref = '/index.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
      pdt = time.strptime(udate, '%Y-%m-%dT%H:%M:%S')
      rdate = time.strftime('%Y-%m-%d', pdt)
      ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
      # print('\n', '\n'.join([mtitl, phref, rdate, imurl, authr, videoid]))
      text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    <img class="preview" data-videoid="https://rutube.ru/play/embed/{videoid}" src="{imurl}" align="left" alt="">
  </a>
  <div class="inlbl text">
    <p><a class="nodecor" href="{phref}">{titl}</a></p>
    <p><i class="smaller2">{authr}</i></p>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, imurl=imurl, rdate=rdate, videoid=videoid, titl=tr_chars(titl, 200), authr=authr)
      if not os.path.exists(os.path.join(cdir, hdr)):
        os.mkdir(os.path.join(cdir, hdr))
      open(os.path.join(cdir, hdr, mtitl + '.md'), 'w', encoding='utf-8', newline='\n').write(text)
      fcount += 1
    print(hdr, url, '(%s)' % (fcount,))

if fcount:
  time.sleep(1)
  update_main(cdir)
  updatelist_main(cdir)
  updateturbo_main(cdir)