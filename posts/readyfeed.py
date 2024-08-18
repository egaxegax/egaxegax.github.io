#!python3
#
# Parse Youtube channel's feed (RSS) .xml page to .md
#

RSSlist = [
  ('Подборка из Youtube/Еда', 'channel_id=UC0K_CP437favZ3maGV06vaw'),   #Телеканал Еда
  # ('Подборка из Youtube/Еда', 'channel_id=UCgeval0um2gyuRhP1qch8Uw'),   #В.Емельяненко
  ('Подборка из Youtube/Работа', 'channel_id=UC8JDt3Vz9WYpAS6b-oVH9xw'),#HandyTeddy
  ('Подборка из Youtube/Работа', 'channel_id=UCCOice03R7HkLOu1CLYsgHA'),#Работа вахтой
  ('Подборка из Youtube/Рок', 'channel_id=UCuRFWlVMAwwP8WerDBQWPBQ'),   #Rock Melody
  ('Подборка из Youtube/Рок', 'channel_id=UCxaaXbw6bVYoChlP4HNIolA'),   #Driving Rock
  ('Подборка из Youtube/Рок', 'playlist_id=PLaqeTZoS9LMrqy7lBTa5IH2sD893YW0La'), #70-80-90 rock music
  ('Подборка из Youtube/Путешествия', 'channel_id=UCXrMdUHkl2taQq4DhPg4etg'), #samsebeskazal
  ('Подборка из Youtube/Фильмы', 'channel_id=UCOD2veMoMj5jy6K0pGt55Bw'),#FILMSTER
  ('Подборка из Youtube/Фильмы', 'channel_id=UC3N4p9X5DjPCH184X-izRwA'),#Watch Movies
  ('Подборка из Youtube/Фильмы', 'channel_id=UC7-_uJKpRJXmsxD2B0idDqg'),#Классика жанра
]

import os, sys, time
import xml.etree.ElementTree as ET
from urllib.request import Request, urlopen

cdir = os.path.dirname(__file__)

sys.path.insert(0, cdir+'/..')
from update import main as update_main
from updatelist import main as updatelist_main, tr, tr_chars, tr_cut

fcount = 0

for hdr, url in RSSlist:
  icount = 0
  feedurl = 'https://www.youtube.com/feeds/videos.xml?'+url
  with urlopen(Request(feedurl, headers={'User-Agent': 'Mozilla/5.0'})) as purl:
    for item in ET.fromstring(purl.read(), parser=ET.XMLParser()).findall('{http://www.w3.org/2005/Atom}entry'):
      titl = item.find('{http://www.w3.org/2005/Atom}title').text
      pdate = item.find('{http://www.w3.org/2005/Atom}published').text
      udate = item.find('{http://www.w3.org/2005/Atom}updated').text
      videoid = item.find('{http://www.youtube.com/xml/schemas/2015}videoId').text
      authr = item.find('{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name').text
      imurl= item.find('{http://search.yahoo.com/mrss/}group/{http://search.yahoo.com/mrss/}thumbnail').get('url')
      mtitl = tr_cut(titl)
      phref = '/posts.html?'+ tr(os.path.basename(hdr)) +'/'+ tr(mtitl)
      pdt = time.strptime(udate, '%Y-%m-%dT%H:%M:%S%z')
      rdate = time.strftime('%Y-%m-%d', pdt)
      pdt = time.strptime(udate, '%Y-%m-%dT%H:%M:%S%z')
      ctime = time.strftime('<!--%Y-%m-%d %H:%M:%S-->', pdt)
      # print('\n', '\n'.join([mtitl, phref, rdate, imurl, authr, videoid]))
      text = """{ctime}
<div class="yb">
  <a class="nodecor" href="{phref}">
    <img class="preview" data-videoid="{videoid}" src="{imurl}" align="middle" alt="">
  </a>
  <div class="inlbl">
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
      icount += 1
    print(hdr, url, '(%s)' % (icount,))

if fcount:
  update_main(cdir)
  updatelist_main(cdir)
  