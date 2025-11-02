#!python3
#
# Parse Youtube channel's feed (RSS) .xml page to .md
#

RSSlist = [
  # ('Подборка из Youtube/Еда', 'channel_id=UC0K_CP437favZ3maGV06vaw'),   #Телеканал Еда
  # ('Подборка из Youtube/Еда', 'channel_id=UCgeval0um2gyuRhP1qch8Uw'),   #В.Емельяненко
  # ('Подборка из Youtube/Еда', 'channel_id=UCbb-qqGdlVS7laUbUOTOXhg'),   #Зона Лазерсона  
  # ('Подборка из Youtube/Киноролики', 'channel_id=UCwHZ11aiUpyTg-wkiKbAqKQ'), #MOVIECLIPS TV
  ('Подборка из Youtube/Работа', 'channel_id=UC8JDt3Vz9WYpAS6b-oVH9xw'),#HandyTeddy
  # ('Подборка из Youtube/Работа', 'channel_id=UC2pn5LT4UFz8gwrQF7VKZDQ'),#Константин Кречетов
  ('Подборка из Youtube/Работа', 'channel_id=UC42cQmihrg0Udqac_P0v2hQ'),#NZT USA
  # ('Подборка из Youtube/Работа', 'channel_id=UCCOice03R7HkLOu1CLYsgHA'),#Работа вахтой
  # ('Подборка из Youtube/Работа', 'channel_id=UCUYrDGMOWF6A40BPK2Wt-eg'),#MAX VOS (Дальнобой США)
  # ('Подборка из Youtube/Релакс', 'channel_id=UCwtHGEAtOm9Jdd1JwvS67gA'),#Fireplace4K (Релакс)
  # ('Подборка из Youtube/Рок', 'channel_id=UCuRFWlVMAwwP8WerDBQWPBQ'),   #Rock Melody
  # ('Подборка из Youtube/Рок', 'channel_id=UCxaaXbw6bVYoChlP4HNIolA'),   #Driving Rock
  # ('Подборка из Youtube/Рок', 'playlist_id=PLaqeTZoS9LMrqy7lBTa5IH2sD893YW0La'), #70-80-90 Rock Music
  # ('Подборка из Youtube/Рок', 'channel_id=UCHpEfiVM3rlXBistGgTPakQ'),   #Music Sky
  # ('Подборка из Youtube/Рок', 'channel_id=UCpL9dvPOAW8l7sruH-3OUMw'),   #80's Rock N Roll
  # ('Подборка из Youtube/Рок', 'channel_id=UCKSClb5P4hMTmNeynTzEm7A'),   #thekorolishut
  # ('Подборка из Youtube/Спорт', 'channel_id=UCNBR-cPlJdqlYE0E0n4xwJA'), #Фабрика Футбола
  ('Подборка из Youtube/Путешествия', 'channel_id=UCXrMdUHkl2taQq4DhPg4etg'), #Samsebeskazal Denis
  # ('Подборка из Youtube/Путешествия', 'channel_id=UCcgTo1grFem37WQAi8QoRxw'), #Вольному Воля
  ('Подборка из Youtube/Жизнь в США', 'channel_id=UCZj_6DMrUPMaQgKIoBOshaA'), #Столица Мира
  ('Подборка из Youtube/Жизнь в США', 'channel_id=UCIwfHT8ap6c6dWm8y06bQSw'), #Такая Жизнь
  ('Подборка из Youtube/Опасные путешествия', 'channel_id=UCrc2oY9Trr97eYNkSbUBlQg'), #ДИГГЕР ДАНИИЛ ДАВЫДОВ
  # ('Подборка из Youtube/Тайны', 'channel_id=UCtIoZ-DVPymIv3t6365uFow'), #Темная сторона
  # ('Подборка из Youtube/Тайны', 'channel_id=UCVsDyCRge9DXmk1S6Ibr10Q'), #Свидетель Windows
  # ('Подборка из Youtube/Тайны', 'channel_id=UCNS8QijmVzXxgWndUb0h1Cw'), #CreepyVids
  # ('Подборка из Youtube/Фильмы', 'channel_id=UCOD2veMoMj5jy6K0pGt55Bw'),#FILMSTER
  # ('Подборка из Youtube/Фильмы', 'channel_id=UC3N4p9X5DjPCH184X-izRwA'),#Watch Movies
  # ('Подборка из Youtube/Фильмы', 'channel_id=UCrZLsQDHEBVSWDadKGQAxHA'),#military_movies
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
  feedurl = 'https://www.youtube.com/feeds/videos.xml?'+url
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
    <img class="preview" data-videoid="https://www.youtube.com/embed/{videoid}" src="{imurl}" align="left" alt="">
  </a>
  <div class="inlbl text">
    <p><a class="nodecor" href="{phref}">{titl}</a></p>
    <p><i class="smaller2">{authr}</i></p>
    <i class="smaller3">{rdate}</i>
  </div>
</div>
""".format(ctime=ctime, phref=phref, imurl=imurl, rdate=rdate, videoid=videoid, titl=tr_chars(titl, 180), authr=authr)
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